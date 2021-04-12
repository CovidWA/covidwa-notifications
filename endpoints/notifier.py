from helpers import database, extract_zip, send_text
from flask import request
import os

from helpers.zip_helpers import get_closest_zips

NUM_TO_SEND = 3  # Default messages to send before needing to renew

def notifier():
    data = request.json

    if not int(os.environ['NOTIFIER_ENABLED']):  # If disabled
        return {'statusCode': 200}
    if data['secret'] != os.environ['NOTIFIER_SECRET']:  # If secret doesn't match
        return {'statusCode': 401, 'body': 'Secret is wrong'}

    site = data['site']
    all_zips = get_closest_zips(extract_zip(site['address']))

    phone_numbers_notified = []

    for zip_code in all_zips:
        for key, user in database.get_where(zip_code=zip_code).items():
            if user['counter_to_renew']:
                counter_to_renew = user['counter_to_renew']
            else:
                # Deal with legacy users who don't have this counter set
                if user['needs_renewal']:
                    counter_to_renew = 0
                else:
                    counter_to_renew = NUM_TO_SEND
            if counter_to_renew < 1:
                continue

            url = f'https://cvd.to/i/{site["id"]}'
            phone_number = user['phone_number']
            message = f'[CovidWA] New availablity for {zip_code}: {site["name"]} {url}. ' \
                'Reply YES to keep receiving notifications.'
            if not data.get('dryRun', False):  # Can send in dryRun flag to not actually send texts
                send_text(phone_number, message)
            print(f'Notified {phone_number} with message "{message}"')
            phone_numbers_notified.append(phone_number)

            counter_to_renew = counter_to_renew - 1
            database.update(key, needs_renewal=(counter_to_renew == 0), counter_to_renew=counter_to_renew)

    body = f'Notified {len(phone_numbers_notified)} numbers: {phone_numbers_notified}'
    return {'statusCode': 200, 'body': body}
