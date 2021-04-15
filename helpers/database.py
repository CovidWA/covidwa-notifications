from dotenv import load_dotenv
from firebase import FirebaseApplication
import os
if __name__ != '__main__':
    from constants import NUM_TO_SEND
else:
    NUM_TO_SEND = 3


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
        query = {'orderBy': f'"{match_k}"', 'equalTo': f'"{match_v}"'}
        query.update(self.params)
        return self.firebase.get('users', None, params=query) or {}

    def post(self, phone_number, zip_code, needs_renewal=False, counter_to_renew=NUM_TO_SEND):
        d = {'phone_number': phone_number, 'zip_code': zip_code, 'needs_renewal': needs_renewal,
             'counter_to_renew': counter_to_renew}
        self.firebase.post('users', d, params=self.params)

    def update(self, id, **kwargs):
        for key, value in kwargs.items():
            self.firebase.put('users', f'{id}/{key}', value, params=self.params)

    def delete(self, id):
        self.firebase.delete('users', id, params=self.params)


load_dotenv()
database = Database()
if __name__ == '__main__':
    users = database.get()
    renewed = 0
    for user in users.values():
        if not user['needs_renewal']:
            renewed += 1
    print('total users:', len(users))
    print('renewed:', renewed)
