import json
import requests


class Database:
    def __init__(self):
        with open('config.json') as file:
            config = json.load(file)
        self.headers = {
            'Authorization': f'Bearer {config["airtable_key"]}',
            'Content-Type': 'application/json'
        }
        self.url = 'https://api.airtable.com/v0/appiGonw4Dnm3zSD1/Users'

    def get(self):
        """Gets all records from the airtable"""
        return requests.get(self.url, headers=self.headers).json()

    def post(self, phone_number, zip_code):
        """Posts phone_number and zip_code as a new record in the airtable"""
        data = {'records': [
            {'fields': {'phone_number': phone_number, 'zip_code': zip_code}}
        ]}
        return requests.post(self.url, json.dumps(data), headers=self.headers)


database = Database()
