from helpers.database import database
from helpers.zip_helpers import is_valid_zip
from flask import request
from twilio.twiml.voice_response import VoiceResponse, Gather


def voice():
    resp = VoiceResponse()

    gather = Gather(num_digits=5, action='/gather')
    gather.say('To receive vaccine notifications, please enter your zip code into the keypad')
    resp.append(gather)

    resp.redirect('/voice')  # If no answer, restart answering

    return str(resp)


def voice_gather():
    resp = VoiceResponse()

    zip_code = request.values['Digits']

    if not is_valid_zip(zip_code):
        gather = Gather(num_digits=5, action='/gather')
        gather.say('Not a valid Washington zip code, please try again')
        resp.append(gather)
        return str(resp)

    say_zip_code = ' '.join(list(zip_code))  # Seperated by spaces
    resp.say(f'You have signed up for vaccine notifications in zip code {say_zip_code}. Thank you and goodbye')

    database.post(request.values.get('From'), zip_code)  # Add user to airtable

    return str(resp)
