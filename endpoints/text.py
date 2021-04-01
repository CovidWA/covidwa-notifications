from helpers.database import database
from helpers.validate_twilio_request import validate_twilio_request
from helpers.zip_helpers import extract_zip
from flask import request
from twilio.twiml.messaging_response import MessagingResponse


@validate_twilio_request
def text():
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

    already_subscribed_response = check_already_subscribed(from_, zip_code)
    if already_subscribed_response is not None:
        return already_subscribed_response

    database.post(from_, zip_code)  # Add user to database

    resp = MessagingResponse()
    resp.message(
        f'You have successfully subscribed for vaccine availability updates in zip code {zip_code}.'
    )
    return str(resp)


def check_keywords(from_, body):
    """Returns a messaging response if needed, None if no keywords"""
    UNSUBSCRIBE_KEYWORDS = ['cancel', 'end', 'quit', 'unsubscribe', 'stop', 'stopall']
    RESUBSCRIBE_KEYWORDS = ['start', 'yes', 'unstop']

    for keyword in UNSUBSCRIBE_KEYWORDS:
        if keyword in body.lower():
            # Remove from database
            user = database.get_where(phone_number=from_)
            if user is not None:
                database.delete(user['id'])
            return str(MessagingResponse())  # No response needed, twilio handles that

    for keyword in RESUBSCRIBE_KEYWORDS:
        if keyword in body.lower():
            return process_resubscribe(from_)


def process_resubscribe(from_):
    user = database.get_where(phone_number=from_)
    if user is not None:  # If already subscribed, renew subscription
        if not user['needs_renewal']:
            # If user doesn't need renewal
            return str(MessagingResponse())

        database.update(user['id'], needs_renewal=False)
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
