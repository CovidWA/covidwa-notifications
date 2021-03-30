from dotenv import load_dotenv
import json
import os
import requests
from time import time


class Database:
    """Represents the airtable specific for this project containing phone_number & zip_code pairs"""
    def __init__(self):
        self.headers = {
            'Authorization': f'Bearer {os.environ["AIRTABLE_KEY"]}',
            'Content-Type': 'application/json'
        }
        self.url = 'https://api.airtable.com/v0/appiGonw4Dnm3zSD1/Users'

    def cache(self):
        print('caching...')
        data = requests.get(self.url, headers=self.headers).json()
        data['time'] = time()
        with open('users_cache.json', 'w') as f:
            f.write(json.dumps(data))

    def get(self):
        """Gets all records from the airtable"""
        if not os.path.exists('users_cache.json'):
            self.cache()
        with open('users_cache.json', 'r') as f:
            data = json.load(f)
            if time() - data['time'] > 60:  # If old data
                self.cache()
            return data

    def post(self, phone_number, zip_code):
        """Posts phone_number and zip_code as a new record in the airtable"""
        data = {'records': [
            {'fields': {'phone_number': phone_number, 'zip_code': zip_code}}
        ]}
        return requests.post(self.url, json.dumps(data), headers=self.headers)

    def delete(self, record_id):
        """Deletes a record based on id"""
        requests.delete(self.url + '/' + record_id, headers=self.headers)


load_dotenv()
database = Database()
if __name__ == '__main__':
    print(database.get())
