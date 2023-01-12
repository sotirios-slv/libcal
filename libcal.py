import os
from dotenv import load_dotenv
from datetime import datetime
import requests
from shared_db import query_database

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

def get_locations():

    locations = get_libcal_information('space/locations')

    return locations

def get_bookings(date=False, days=365, page=1, limit=500):

    if not date:
        date = datetime.today().strftime('%Y-%m-%d')

    bookings = get_libcal_information(f'space/bookings?date={date}&days={days}&limit={limit}&date={date}&page={page}')

    return bookings

# Query locations API and save id and room name into memory


# Get most recent date added
sql_statement = """
select date
from public.slv_data
where project = 'libcal'
ORDER BY date DESC
LIMIT 1
"""
top_date_in_db = query_database(sql_statement, return_data=True)

print(top_date_in_db)

# Query bookings API from most recent date added recursively using page param until len of returned values is less than limit

# Commit to DB

# Disconnect from DB