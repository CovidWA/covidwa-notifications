# Covidwa Notifications

Users can sign up via text and will get notified when covidwa detects a site near them has new availability.

# Quick Start

## Setup

### Python
- `pip install -r requirements.txt` to install package dependencies

### Twilio
- Register with Twilio, choose trial account
- "Purchase" phone number with trial dollars
- Fill in `account_sid`, `auth_token`, and `phone_number` fields in `config.json`

### Config
Create a `config.json` that should look like
```javascript
{
    "account_sid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", // Twilio account sid
    "auth_token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", // Twilio account auth token
    "phone_number": "+12061231234", // Twilio phone number
    "airtable_key": "keyxxxxxxxxxxxxxx" // Your airtable key if you have editor access to the airtable
}
```

## Run

### Run notifier
The notifier scans for sites with new availability and texts people in the zip code
- `cd src`
- Run `python notifier.py`
- Make sure the `airtable_key` is set in `config.json`

### Run the twilio app (for text to sign up)
- Install ngrok from https://ngrok.com
- `cd src`
- Start the flask app with `python app.py` which will run on port 5000
- Make your localhost public with `ngrok http 5000`. Copy your url: `https://58afd968e95a.ngrok.io`
- Copy your url into the twilio phone number webhook for text (`https://58afd968e95a.ngrok.io/text`) and call (`https://58afd968e95a.ngrok.io/voice`)
- Now try calling or texting your zip code to the twilio number and you should be signed up and added to the airtable
