"""
API_FIELDS dictionary is used to help configure the fields that are returned during the call to the booking API, as well as any headers included in an exported csv file of that data

The 'datetime_fields' list are treated differently in as much as they are split into constituent date and time columns. 
!It is important that the first entry in the datetime_fields list is the 'fromDate' because it's used as part of the recursive API call. 
"""

API_FIELDS = {
    "non_date_fields" : [
        "bookId",
        "eid",
        "location_name",
        "category_name",
        "status"
    ],
    "datetime_fields" : [
        "fromDate",
        "toDate",
        "created"
    ]
}