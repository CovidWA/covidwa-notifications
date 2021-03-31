# https://www.twilio.com/docs/usage/tutorials/how-to-secure-your-flask-app-by-validating-incoming-twilio-requests
from flask import abort, request
from functools import wraps
import os
from twilio.request_validator import RequestValidator


def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        validator = RequestValidator(os.environ.get('AUTH_TOKEN'))

        # Validate the request using its URL, POST data, and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            request.url,
            request.form,
            request.headers.get('X-TWILIO-SIGNATURE', ''))

        # Call decorated function if it's valid and return a 403 error if not
        if request_valid:
            return f(*args, **kwargs)
        else:
            return abort(403)

    return decorated_function
