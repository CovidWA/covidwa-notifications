from helpers.database import database
from helpers.validate_twilio_request import validate_twilio_request
from helpers.zip_helpers import extract_zip
from flask import request
from twilio.twiml.messaging_response import MessagingResponse


@validate_twilio_request
def text():
    from_ = request.values['From']
    body = request.values['Body']

    resp = MessagingResponse()

    zip_code = extract_zip(body)
    if zip_code is None:  # If no zip code provided or it's invalid
        resp.message('No valid WA zip code detected. Please try again.')
        return str(resp)

    database.post(from_, zip_code)  # Add user to airtable

    resp = MessagingResponse()
    resp.message('You have successfully subscribed for vaccine availability updates.')
    return str(resp)
