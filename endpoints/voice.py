from helpers import database, is_valid_zip, get_balance, validate_twilio_request
from flask import abort, request
from twilio.twiml.voice_response import VoiceResponse, Gather


@validate_twilio_request
def voice():
    if get_balance() <= 30:
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


def check_already_subscribed(from_, zip_code):
    for key, user in database.get().items():
        if user['phone_number'] == from_:  # If already subscribed
            resp = VoiceResponse()
            say_zip_code = ' '.join(list(user["zip_code"]))  # Seperated by spaces
            say_new_zip_code = ' '.join(list(zip_code))  # Seperated by spaces
            resp.say(
                f'You have switched your zip code from {say_zip_code} to {say_new_zip_code}. Thank you and goodbye'
            )

            database.update(key, zip_code=zip_code)

            return str(resp)
