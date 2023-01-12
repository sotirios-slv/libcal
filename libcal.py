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

    # print(r.status_code)
    print(r.json()[0])

    for t in r.json()[0].keys():
        print(t)

# get_libcal_information('calendars')
# get_libcal_information('events?cal_id=11060')
# get_libcal_information('space/bookings?date=2020-01-01&days=7')
get_libcal_information('space/locations')

# libcalEndpoint = "https://slv-vic.libcal.com/1.1/space/bookings?limit=500&formAnswers=1&date="+ydate
# libcalLocations = "https://slv-vic.libcal.com/1.1/space/locations"