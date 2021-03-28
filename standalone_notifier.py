"""Not being used because currently using api endpoint /notifier"""
import json
import os
import requests
from collections import defaultdict
from helpers.database import database
from helpers.sms_api import send_text
from helpers.zip_helpers import extract_zip


class Notifier():
    def __init__(self):
        self.all_availabile_ids = []
        self.zip_availability_map = defaultdict(int)  # {zip_code: num_clinics_available, ...}
        self.clinic_records = {}  # {id: record, ...}
        self.load_clinic_records()

        if not os.path.exists('lastRunAvailableIds.json'):  # If is first run
            # This is done so it doesn't think that all clinics are newly available
            print('First run, initializing lastRunAvailableids.json to reflect current records')
            self.save_available_ids()

        self.new_available_ids = self.get_new_available_ids()
        print(f'Number of newly available sites: {len(self.new_available_ids)}')
        self.zip_url_map = {}  # {zip_code: url, ...}
        self.zips_to_notify = self.get_zips_to_notify()
        print(f'Notifying zips: {self.zips_to_notify}')
        self.send_texts()

        self.save_available_ids()

    def load_clinic_records(self):
        """Loads clinic data from covidwa site and processes it"""
        records = requests.get('https://api.covidwa.com/v1/get').json()['data']
        for record in records:
            if 'address' not in record:
                continue
            self.clinic_records[record['id']] = record

        for id, record in self.clinic_records.items():
            if record['Availability'] == 'Yes':
                record['zip_code'] = extract_zip(record['address'])

                self.all_availabile_ids.append(id)

                self.zip_availability_map[record['zip_code']] += 1

    def get_new_available_ids(self):
        """Returns a list with ids that are available now but weren't last run"""
        new_available_ids = []
        with open('lastRunAvailableIds.json', 'r') as file:
            last_available_ids = json.load(file)

            for available_id in self.all_availabile_ids:
                if available_id not in last_available_ids:
                    new_available_ids.append(available_id)

        return new_available_ids

    def get_zips_to_notify(self):
        """Returns a list of zip codes that pass the following conditions:
        - Have an appointment with new availability
        - Have no other site with availability
        - TODO: possibly notify people in other close zip codes
        - TODO: cap the number of people notified
        """
        zips_to_notify = []
        for new_available_id in self.new_available_ids:
            zip_code = self.clinic_records[new_available_id]['zip_code']

            if self.zip_availability_map[zip_code] > 1:
                continue  # If there were already appointments in this zip

            url = self.clinic_records[new_available_id]['url']
            self.zip_url_map[zip_code] = url
            zips_to_notify.append(zip_code)

        return zips_to_notify

    def send_texts(self):
        """Sends texts to users based on self.zips_to_notify"""
        print('Users notified:')
        for user in database.get()['records']:
            zip_code = user['fields']['zip_code']
            if zip_code in self.zips_to_notify:
                url = self.zip_url_map[zip_code]
                phone_number = user['fields']['phone_number']
                # TODO: send more info about the clinic
                send_text(phone_number, f'There are new appointments in zip code: {zip_code}. Sign up with: {url}')
                print(f'- Notified phone number: {phone_number} in zip code: {zip_code}')

    def save_available_ids(self):
        """Stores availabile ids in a file to check in future runs"""
        with open('lastRunAvailableIds.json', 'w') as file:
            json.dump(self.all_availabile_ids, file)


if __name__ == '__main__':
    Notifier()
