from helpers.database import database
from helpers.zip_helpers import extract_zip
from helpers.sms_api import send_text
from flask import request
import os


def notifier():
    data = request.json

    if not int(os.environ['NOTIFIER_ENABLED']):  # If disabled
        return {'statusCode': 200}
    if data['secret'] != os.environ['NOTIFIER_SECRET']:  # If secret doesn't match
        return {'statusCode': 401, 'body': 'Secret is wrong'}

    site = data['site']
    zip_code = extract_zip(site['address'])

    phone_numbers_notified = []
    for user in database.get().values():
        if user['zip_code'] != zip_code:  # If user not in zip code
            continue
        # TODO: expand to zip codes that are close

        url = f'https://cvd.to/i/{site["id"]}'
        phone_number = user['phone_number']
        if phone_number in phone_numbers_notified:
            continue  # Don't notify same person twice

        message = f'There are new appointments in zip code: {zip_code} - {site["name"]} {url}'
        if not data.get('dryRun', False):  # Can send in dryRun flag to not actually send texts
            send_text(phone_number, message)
        phone_numbers_notified.append(phone_number)
        print(f'Notified {phone_number} with message "{message}"')

    body = f'Notified {len(phone_numbers_notified)} numbers: {phone_numbers_notified}'
    return {'statusCode': 200, 'body': body}
