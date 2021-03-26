import os
import twilio
from twilio.rest import Client


def send_text(to, body):
    client = Client(os.environ['account_sid'], os.environ['auth_token'])
    try:
        client.messages.create(body=body, from_=os.environ['phone_number'], to=to)
    except twilio.base.exceptions.TwilioRestException:
        print('ERROR: twilio credentials invalid')
