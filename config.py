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


API_FIELDS_MAP = {
    "bookId" : "Booking ID",
    "eid" : "Space ID",
    "item_name" : "Space/Seat Name",
    "location_name" : "Location",
    "category_name" : "Category",
    "fromDate" : ["From Date", "From Time"],
    "toDate" : ["To Date", "To Time"],
    "created" : ["Created Date", "Created Time"],
    "status" : "Status",
}