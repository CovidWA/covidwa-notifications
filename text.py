from database import database
from flask import request
from twilio.twiml.messaging_response import MessagingResponse
from zip_helpers import extract_zip


def respond():
    from_ = request.values.get('From')
    body = request.values.get('Body')

    resp = MessagingResponse()

    zip_code = extract_zip(body)
    if zip_code is None:  # If no zip code provided or it's invalid
        if 'unsubscribe' in body:
            return unsubscribe(from_)
        resp.message('No valid WA zip code detected. Please try again.')
        return str(resp)

    database.post(from_, zip_code)  # Add user to airtable

    resp = MessagingResponse()
    resp.message('You have successfully subscribed for vaccine availability updates.')
    return str(resp)


def unsubscribe(phone_number):
    resp = MessagingResponse()

    ids_to_remove = []
    for user in database.get()['records']:
        if user['fields']['phone_number'] == phone_number:
            ids_to_remove.append(user['recordId'])

    for record_id in ids_to_remove:
        database.delete(record_id)

    resp.message(f'You have successfully unsubscribed from {len(ids_to_remove)} zip codes')
