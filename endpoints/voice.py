from .common import check_already_subscribed
from helpers import database, is_valid_zip, get_balance, validate_twilio_request
from flask import abort, request
from twilio.twiml.voice_response import VoiceResponse, Gather


@validate_twilio_request
def voice():
    if get_balance() <= 0:
        return abort(503)

    resp = VoiceResponse()

    gather = Gather(num_digits=5, action='/gather')
    gather.say('To receive vaccine notifications, please enter your zip code into the keypad')
    resp.append(gather)

    resp.redirect('/voice')  # If no answer, restart answering

    return str(resp)


def voice_gather():
    """Gather the zip code of the caller"""
    resp = VoiceResponse()

    from_ = request.values['From']
    zip_code = request.values['Digits']

    if not is_valid_zip(zip_code):
        gather = Gather(num_digits=5, action='/gather')
        gather.say('Not a valid Washington zip code, please try again')
        resp.append(gather)
        return str(resp)  # Redo

    already_subscribed_response = check_already_subscribed(from_, zip_code)
    if already_subscribed_response is not None:
        return already_subscribed_response

    say_zip_code = ' '.join(list(zip_code))  # Seperated by spaces
    resp.say(f'You have signed up for vaccine notifications in zip code {say_zip_code}. Thank you and goodbye')

    database.post(from_, zip_code)  # Add user to database

    return str(resp)
