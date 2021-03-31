from dotenv import load_dotenv
from firebase import FirebaseApplication
import os


class Database:
    """Represents the Firebase specific for this project containing phone_number & zip_code pairs"""
    def __init__(self):
        url = 'https://covidwa-notifications-default-rtdb.firebaseio.com'
        self.firebase = FirebaseApplication(url, None)
        self.params = {'auth': os.environ['FIREBASE_AUTH']}

    def get(self):
        return self.firebase.get('users', None, params=self.params)

    def post(self, phone_number, zip_code):
        d = {'phone_number': phone_number, 'zip_code': zip_code}
        self.firebase.post('users', d, params=self.params)

    def delete(self, id):
        self.firebase.delete('users', id, params=self.params)


database = Database()
if __name__ == '__main__':
    load_dotenv()
    print(database.get())
