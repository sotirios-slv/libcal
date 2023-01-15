import os
from dotenv import load_dotenv
from datetime import date, timedelta, datetime
import requests
from shared_helpers import query_database, export_to_csv

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
        date = date.today().strftime('%Y-%m-%d')

    bookings = get_libcal_information(f'space/bookings?date={date}&days={days}&limit={limit}&date={date}&page={page}')

    return bookings


# Query locations API and save id and room name into memory
# locations = get_locations()
# print(locations)

# Get most recent date added
# todo: wrap in function
sql_statement = """
select date
from public.slv_data
where project = 'libcal'
ORDER BY date DESC
LIMIT 1
"""
top_date_in_db = query_database(sql_statement, return_data=True)
if not top_date_in_db:
    print('Could not retrieve most recent date from database')

# check date of most recent booking, this is to prevent an infinite loop if there's no booking for 'today'
# todo: wrap in function
date_to_check = date.today()
most_recent_bookings = get_bookings(date=date_to_check,limit=1,days=1)
while len(most_recent_bookings) == 0:
    date_to_check = date_to_check - timedelta(days=1)
    most_recent_bookings = get_bookings(date=date_to_check,limit=1,days=1)


print(date_to_check)
# Calculate no. of days since last update. If it's less than the APIs max days (365) add to the query param
last_date_retrieved = top_date_in_db[0][0]

booking_dates = []
returned_values_upload_list = []

days_since_last_update = 1
while days_since_last_update > 0:
    
    # todo: wrap in function
    days_since_last_update = date_to_check - last_date_retrieved
    days_since_last_update = int(days_since_last_update.days)
    print('Days: ', days_since_last_update)
    days = min(days_since_last_update,365)

    # Query bookings API from most recent date added recursively using page param until len of returned values is less than limit
    # Do not include any bookings after 'today'
    page_counter = 1
    bookings_info = get_bookings(date=last_date_retrieved,days=days, page=page_counter)

    #  Date returned from LibCal API in following format: 2021-11-10T10:00:00+11:00
    from_dates = [datetime.strptime(booking['fromDate'],'%Y-%m-%dT%H:%M:%S%z') for booking in bookings_info]
    booking_dates.extend(from_dates)

    value_for_upload = [[datetime.strptime(booking['fromDate'],'%Y-%m-%dT%H:%M:%S%z'),'visitor','libcal','booking',booking.get('location_name',''),booking.get('item_name',''),booking.get('item_id',''),booking.get('item_status','')] for booking in bookings_info]
    returned_values_upload_list.extend(value_for_upload)

    while len(bookings_info) > 0:
        page_counter += 1
        bookings_info = get_bookings(date=last_date_retrieved,days=days, page=page_counter)
        from_dates = [datetime.strptime(booking['fromDate'],'%Y-%m-%dT%H:%M:%S%z') for booking in bookings_info] # todo: need to add more flexibility if key not found
        value_for_upload = [[datetime.strptime(booking['fromDate'],'%Y-%m-%dT%H:%M:%S%z'),'visitor','libcal','booking',booking.get('location_name',''),booking.get('item_name',''),booking.get('item_id',''),booking.get('item_status','')] for booking in bookings_info]

        booking_dates.extend(from_dates)
        returned_values_upload_list.extend(value_for_upload)

    last_date_retrieved = max(booking_dates).date()

print(len(booking_dates))

# default_values = [[str(booking.date()),'visitor','libcal','booking'] for booking in booking_dates]
# combined_values = zip(default_values,returned_values_upload_list)

# print('Default: ', len(combined_values))
export_to_csv('exports/booking_dates', returned_values_upload_list)






# Commit to DB

# Disconnect from DB