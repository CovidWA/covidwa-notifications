from database import database
from flask import request, jsonify
import os
from sms_api import send_text
from zip_helpers import extract_zip


def notify(data=None):
    if data is None:
        data = request.json

    if not int(os.environ['NOTIFIER_ENABLED']):
        return {'statusCode': 200}
    if data['secret'] != os.environ['NOTIFIER_SECRET']:
        return {'statusCode': 401, 'body': 'Secret is wrong'}

    site = data['site']
    zip_code = extract_zip(site['address'])

    phone_numbers_notified = []
    for user in database.get()['records']:
        if user['fields']['zip_code'] != zip_code:  # TODO: expand to near zip codes
            continue

        url = f'https://cvd.to/i/{site["id"]}'
        phone_number = user['fields']['phone_number']
        if phone_number in phone_numbers_notified:
            continue  # Don't notify same person twice

        message = f'There are new appointments in zip code: {zip_code} - {site["name"]} {url}'
        if data.get('dryRun', False):
            send_text(phone_number, message)
        phone_numbers_notified.append(phone_number)
        print(f'Notified {phone_number} with message "{message}"')

    return {'statusCode': 200}


if __name__ == '__main__':
    data = {
        "secret": os.environ['NOTIFIER_SECRET'],
        "site": {
            "name": "Bla in Kent",
            "address": "19300 108th Ave SE, Kent, WA 98105",
            "id": "recuSvlxQazPBrLez",
        },
        "dryRun": True
    }
    # notify(data)
    import requests, json
    requests.post('https://covidwa-notifications.herokuapp.com/notifier', json.dumps(data), headers={'Content-Type': 'application/json'})
