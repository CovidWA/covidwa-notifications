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

    def get(self):
        return self.firebase.get('users', None, params=self.params) or {}

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
    print(database.get())
