from dotenv import load_dotenv
from firebase import FirebaseApplication
import json
import os
from time import time


class Database:
    """Represents the Firebase specific for this project containing phone_number & zip_code pairs"""
    def __init__(self):
        url = 'https://covidwa-notifications-default-rtdb.firebaseio.com'
        self.firebase = FirebaseApplication(url, None)
        self.params = {'auth': os.environ['FIREBASE_AUTH']}

    def cache(self):
        print('caching users...')
        with open('users_cache.json', 'w') as f:
            d = {
                'data': self.firebase.get('users', None, params=self.params),
                'time': time()
            }
            json.dump(d, f)
        return d

    def get(self):
        if not os.path.exists('users_cache.json'):
            self.cache()
        with open('users_cache.json', 'r') as f:
            d = json.load(f)
            if time() - d['time'] > 60:  # If old data
                d = self.cache()
            return d['data']

    def post(self, phone_number, zip_code):
        d = {'phone_number': phone_number, 'zip_code': zip_code}
        self.firebase.post('users', d, params=self.params)

    def delete(self, id):
        self.firebase.delete('users', id, params=self.params)


load_dotenv()
database = Database()
if __name__ == '__main__':
    print(database.get())
