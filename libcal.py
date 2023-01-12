import os
from dotenv import load_dotenv

import requests

load_dotenv
libcal_url = os.environ.get('LIBCAL_URL')
libcal_client_secret = os.environ.get('LIBCAL_CLIENT_SECRET')
libcal_client_id = os.environ.get('LIBCAL_CLIENT_ID')

def get_access_token():

    payload = {
        "client_id" : libcal_client_id,
        "client_secret" : libcal_client_secret,
        "grant_type" : "client_credentials"
    }

    r = requests.post(f'{libcal_url}oauth/token', json=payload)

    if r.status_code != 200:
        return False
    
    access_token = r.json()['access_token']

    return access_token

def get_libcal_information(endpoint):

    access_token = get_access_token()
    
    if not access_token:
        return False

    headers = {
        "Authorization" : f'Bearer {access_token}'
    }
    
    r = requests.get(f'{libcal_url}{endpoint}', headers=headers)

    if r.status_code != 200:
        print(r.text)
        return False
    
    return r.json()

# Connect to DB

# Query locations API and save id and room name into memory

# Get most recent date added

# Query bookings API from most recent date added recursively using page param until len of returned values is less than limit

# Commit to DB

# Disconnect from DB

# get_libcal_information('space/bookings?date=2020-01-01&days=7')
print(get_libcal_information('space/locations'))

# libcalEndpoint = "https://slv-vic.libcal.com/1.1/space/bookings?limit=500&formAnswers=1&date="+ydate
# libcalLocations = "https://slv-vic.libcal.com/1.1/space/locations"