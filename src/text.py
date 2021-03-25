from database import database
from flask import request
from zip_helpers import extract_zip
from twilio.twiml.messaging_response import MessagingResponse


def respond():
    from_ = request.values.get('From')
    body = request.values.get('Body')

    resp = MessagingResponse()

    zip_code = extract_zip(body)
    if zip_code is None:  # If no zip code provided or it's invalid
        resp.message('No valid WA zip code detected. Please try again.')
        return str(resp)

    database.post(from_, zip_code)  # Add user to airtable

    resp = MessagingResponse()
    resp.message('You have successfully subscribed for vaccine availability updates.')
    return str(resp)
