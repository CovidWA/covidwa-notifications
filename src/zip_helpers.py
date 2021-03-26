import json
import re


def is_valid_zip(zip_code):
    """Returns whether or not the zip code is a valid WA zip code"""
    with open('../zipLocations.json') as f:
        data = json.load(f)
    all_zips = data.keys()
    return zip_code in all_zips


def extract_zip(s):
    """Returns a valid zip code from a string"""
    for match in re.findall(r'\d{5}', s):
        if is_valid_zip(match):
            return match
