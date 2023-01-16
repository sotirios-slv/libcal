"""
DB column : API field
Booking ID : bookId
Space ID : eid
Space/Seat Name
Location: location_name
Zone: ?
Category: category_name
From Date: fromDate (split)
From Time: fromDate (split)
To Date: toDate (split)
To Time: toDate (split)
Created Date: created (split)
Created Time: created (split)
Status: status
Checked In Date: 
Checked In Time
Booking Form Answers
"""


API_FIELDS_TO_RETURN = [
        "bookId",
        "eid",
        "location_name",
        "category_name",
        "fromDate",
        "toDate",
        "created",
        "status"
    ]