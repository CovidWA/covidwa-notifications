import os
import twilio
from twilio.rest import Client


def send_text(to, body):
    client = Client(os.environ['ACCOUNT_SID'], os.environ['AUTH_TOKEN'])
    try:
        client.messages.create(body=body, from_=os.environ['PHONE_NUMBER'], to=to)
    except twilio.base.exceptions.TwilioRestException:
        print('ERROR: twilio credentials invalid')
