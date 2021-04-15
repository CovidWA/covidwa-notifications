from endpoints.notifier import NUM_TO_SEND
from helpers import database, extract_zip, get_balance, validate_twilio_request
from flask import abort, request
import requests
from twilio.twiml.messaging_response import MessagingResponse


@validate_twilio_request
def text():
    # if get_balance() <= 30:
    #     return abort(503)

    from_ = request.values['From']
    body = request.values['Body']

    keywords_response = check_keywords(from_, body)
    if keywords_response is not None:
        return keywords_response

    zip_code = extract_zip(body)
    if zip_code is None:  # If no zip code provided or it's invalid
        resp = MessagingResponse()
        resp.message('No valid WA zip code detected. Please try again.')
        return str(resp)

    if not has_locations(zip_code):
        resp = MessagingResponse()
        resp.message('Sorry, there are no tracked locations in that zip code. Please try a different zip code')
        return str(resp)

    already_subscribed_response = check_already_subscribed(from_, zip_code)
    if already_subscribed_response is not None:
        return already_subscribed_response

    database.post(from_, zip_code)  # Add user to database

    resp = MessagingResponse()
    resp.message(
        f'You have successfully subscribed for CovidWA vaccine availability updates in zip code {zip_code}.'
    )
    return str(resp)


def check_keywords(from_, body):
    """Returns a messaging response if needed, None if no keywords"""
    UNSUBSCRIBE_KEYWORDS = ['cancel', 'end', 'quit', 'unsubscribe', 'stop', 'stopall']
    RESUBSCRIBE_KEYWORDS = ['start', 'yes', 'unstop']

    for keyword in UNSUBSCRIBE_KEYWORDS:
        if keyword in body.lower():
            # Remove from database
            user_id, user = list(database.get_where(phone_number=from_).items())[0]
            if user is not None:
                database.delete(user_id)
            return str(MessagingResponse())  # No response needed, twilio handles that

    for keyword in RESUBSCRIBE_KEYWORDS:
        if keyword in body.lower():
            return process_resubscribe(from_)


def process_resubscribe(from_):
    user_find_results = list(database.get_where(phone_number=from_).items())
    if user_find_results != []:  # If already subscribed, renew subscription
        user_id, user = user_find_results[0]
        if not user['needs_renewal']:
            # If user doesn't need renewal
            return str(MessagingResponse())

        database.update(user_id, needs_renewal=False, counter_to_renew=NUM_TO_SEND)
        print(from_, 'renewed')
        resp = MessagingResponse()
        resp.message(f'You will continue receiving notifications for zip code {user["zip_code"]}')
        return str(resp)

    resp = MessagingResponse()
    resp.message('Please send your zip code to resubscribe')
    return str(resp)


def check_already_subscribed(from_, zip_code):
    for key, user in database.get().items():
        if user['phone_number'] == from_:  # If already subscribed
            resp = MessagingResponse()
            resp.message(
                f'You have switched your zip code from {user["zip_code"]} to {zip_code}'
            )

            database.update(key, zip_code=zip_code)

            return str(resp)


def has_locations(zip_code):
    data = requests.get('https://api.covidwa.com/v1/get').json()['data']
    for location in data:
        if extract_zip(location.get('address', '')) == zip_code:
            return True
    return False
