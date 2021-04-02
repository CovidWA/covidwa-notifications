from helpers import database, extract_zip, send_text
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

    for key, user in database.get().items():
        if user['zip_code'] != zip_code:  # If user not in zip code
            continue

        url = f'https://cvd.to/i/{site["id"]}'
        phone_number = user['phone_number']

        if user['needs_renewal']:
            continue  # If already notified and not renewed

        message = f'There are new appointments in zip code: {zip_code} - {site["name"]} {url}. ' \
            'Reply YES to keep receiving notifications.'
        if not data.get('dryRun', False):  # Can send in dryRun flag to not actually send texts
            send_text(phone_number, message)
        print(f'Notified {phone_number} with message "{message}"')
        phone_numbers_notified.append(phone_number)

        database.update(key, needs_renewal=True)

    body = f'Notified {len(phone_numbers_notified)} numbers: {phone_numbers_notified}'
    return {'statusCode': 200, 'body': body}
