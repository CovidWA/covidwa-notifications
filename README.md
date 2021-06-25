:warning: This project is no longer running or being maintained, because of widespread vaccine
availability

# CovidWA Notifications

## Usage

Sign up by sending you zip code to the phone number (206) 222-9793. When there is new vaccine
appointment availability in your area, you will get a text with a link to schedule your appointment.

## How it works

Python Flask app hosted by Heroku, has webhooks (endpoints `/text` and `/voice`) that receive texts
and calls from Twilio. People sign up, and it adds their phone number and zip code to the Firebase
database. The `/notifier` endpoint is posted to by the covidwa.com backend, and uses the database
to decide who to send notifications to via text using Twilio.
