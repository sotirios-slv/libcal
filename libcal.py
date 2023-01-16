import os
from dotenv import load_dotenv
from datetime import date, timedelta, datetime
import requests
from shared_helpers import export_to_csv, get_most_recent_date_in_db

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

def get_bookings(date_to_retrieve=False, days=365, page=1, limit=500):

    if not date_to_retrieve:
        date_to_retrieve = date.today().strftime('%Y-%m-%d')

    bookings = get_libcal_information(f'space/bookings?date={date_to_retrieve}&days={days}&limit={limit}&page={page}')

    return bookings


# check date of most recent booking, this is to prevent an infinite loop if there's no booking for 'today'
# todo: wrap in function
date_to_check = date.today()
most_recent_bookings = get_bookings(date_to_retrieve=date_to_check,limit=1,days=1)
while len(most_recent_bookings) == 0:
    date_to_check = date_to_check - timedelta(days=1)
    most_recent_bookings = get_bookings(date=date_to_check,limit=1,days=1)

# Calculate no. of days since last update. If it's less than the APIs max days (365) add to the query param
last_date_retrieved = get_most_recent_date_in_db()

returned_values_upload_list = []

days_since_last_update = 1
while days_since_last_update > 0:
    
    # todo: wrap in function
    days_since_last_update = date_to_check - last_date_retrieved
    days_since_last_update = int(days_since_last_update.days)
    days = min(days_since_last_update,365)

    # Query bookings API from most recent date added recursively using page param until len of returned values is less than limit
    # Do not include any bookings after 'today'
    page_counter = 1
    bookings_info = get_bookings(date_to_retrieve=last_date_retrieved,days=days, page=page_counter)

    #  Date returned from LibCal API in following format e.g. 2021-11-10T10:00:00+11:00
    values_for_upload = [[datetime.strptime(booking['fromDate'],'%Y-%m-%dT%H:%M:%S%z'),'visitor','libcal','booking',booking.get('location_name',''),booking.get('item_name',''),booking.get('item_id',''),booking.get('item_status','')] for booking in bookings_info]
    returned_values_upload_list.extend(values_for_upload)

    while len(bookings_info) > 0:
        page_counter += 1
        bookings_info = get_bookings(date_to_retrieve=last_date_retrieved,days=days, page=page_counter)
        # todo: need to add a further if key not found
        values_for_upload = [[datetime.strptime(booking['fromDate'],'%Y-%m-%dT%H:%M:%S%z'),'visitor','libcal','booking',booking.get('location_name',''),booking.get('item_name',''),booking.get('item_id',''),booking.get('item_status','')] for booking in bookings_info]

        returned_values_upload_list.extend(values_for_upload)

    # Complicated one-liner to get the most recent date:
    last_date_retrieved = max([element[0].date() for element in returned_values_upload_list])


# export_to_csv('exports/booking_dates', returned_values_upload_list)






# Commit to DB

# Disconnect from DB