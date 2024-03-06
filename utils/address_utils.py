import re
import requests

base_url = "https://api.postcodes.io"


def postcode_url(city):
    return base_url + "/postcodes/" + city


def is_postcode(address):
    return (
        re.fullmatch(r"[A-Za-z][A-Za-z0-9]{1,3}\s*[0-9][A-Za-z]{2}", address)
        is not None
    )


def is_in_region(address, region):
    try:
        return (
            is_postcode_in_region(address, region)
            if is_postcode(address)
            else region.lower() in address.lower() or address.lower() in region.lower()
        )
    except Exception as e:
        return False


def is_postcode_in_region(postcode, region):
    if postcode.lower() == region.lower():
        return True
    postcode_response = requests.get(postcode_url(postcode))
    if postcode_response.status_code == 200:
        return any(
            region.lower() in str(val).lower()
            for val in postcode_response.json()["result"].values()
        )
    else:
        raise Exception(
            f"Error: {postcode_response.status_code}, {postcode_response.json()}"
        )
