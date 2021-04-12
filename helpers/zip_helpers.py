import re

from zip_locations import ALL_ZIPS

def is_valid_zip(zip_code):
    """Returns whether or not the zip code is a valid WA zip code"""
    return zip_code in ALL_ZIPS


def extract_zip(s):
    """Returns a valid zip code from a string"""
    for match in re.findall(r'\d{5}', s):
        if is_valid_zip(match):
            return match

DEFAULT_NEARBY_COORD = 0.005  # Roughly 5 miles
def get_closest_zips(zip, distance=DEFAULT_NEARBY_COORD):
    """Returns a list of nearby zips, including the input zip"""
    long, lat = ALL_ZIPS[zip]
    zips = []
    for zip2, coord in ALL_ZIPS.items():
        if (abs(coord[0]-long)**2 + abs(coord[1]-lat)**2 < distance):
            zips.append(zip2)
    return zips
