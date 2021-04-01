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
        open('notified_before_next_cache.csv', 'w').close()  # Clear file
        with open('users_cache.json', 'w') as f:
            d = {
                'data': self.firebase.get('users', None, params=self.params),
                'time': time()
            }
            if d['data'] is None:
                d['data'] = {}
            json.dump(d, f)
        return d

    def get(self, use_cache=True):
        if not use_cache:
            return self.firebase.get('users', None, params=self.params)

        if not os.path.exists('users_cache.json'):
            self.cache()
        with open('users_cache.json', 'r') as f:
            d = json.load(f)
            if time() - d['time'] > 60:  # If old data
                d = self.cache()
            return d['data']

    def get_where(self, **kwargs):
        """Returns a user that satisfies condition given by kwarg (e.g. zip_code='12345')"""
        assert len(kwargs) == 1
        match_k, match_v = list(kwargs.items())[0]
        for key, user in self.get().items():
            user['id'] = key
            if user[match_k] == match_v:
                return user

    def post(self, phone_number, zip_code, needs_renewal=False):
        d = {'phone_number': phone_number, 'zip_code': zip_code, 'needs_renewal': needs_renewal}
        self.firebase.post('users', d, params=self.params)

    def update(self, id, **kwargs):
        for key, value in kwargs.items():
            self.firebase.put('users', f'{id}/{key}', value, params=self.params)

    def delete(self, id):
        self.firebase.delete('users', id, params=self.params)


load_dotenv()
database = Database()
if __name__ == '__main__':
    print(database.get(use_cache=False))
