import json
import twilio
from twilio.rest import Client


def send_text(to, body):
    with open('config.json') as file:
        config = json.load(file)
    client = Client(config['account_sid'], config['auth_token'])
    try:
        client.messages.create(body=body, from_=config['phone_number'], to=to)
    except twilio.base.exceptions.TwilioRestException:
        print('ERROR: twilio credentials invalid')
