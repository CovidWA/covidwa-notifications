from helpers import database
from twilio.twiml.messaging_response import MessagingResponse


def check_already_subscribed(from_, zip_code):
    for key, user in database.get().items():
        if user['phone_number'] == from_:  # If already subscribed
            resp = MessagingResponse()
            resp.message(
                f'You have switched your zip code from {user["zip_code"]} to {zip_code}'
            )

            database.update(key, zip_code=zip_code)

            return str(resp)
