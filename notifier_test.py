"""Tests the /notifier endpoint by sending a post request"""
from dotenv import load_dotenv
import json
import os
import requests


if __name__ == '__main__':
    load_dotenv()
    data = {
        'secret': os.environ['NOTIFIER_SECRET'],
        'site': {
            'name': 'Bla in Kent',
            'address': '19300 108th Ave SE, Kent, WA 98105',
            'id': 'recuSvlxQazPBrLez',
        },
        'dryRun': True
    }
    print(requests.post(
        'https://covidwa-notifications.herokuapp.com/notifier',
        json.dumps(data), headers={'Content-Type': 'application/json'}
    ).text)
