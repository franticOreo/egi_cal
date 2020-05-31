# egi_cal
###### Creates Google Doc Invoices for my business, Eli's Garden Improvements

#### Goal
Automate invoice creation from calendar entry.

#### Methodology
This project reads past Google Calendar entries with the Google Calendar API. This calendar information is then parsed and matched to the relevent customers information to a SQL database (SQLite3). This is combined into a invoice dictionary which is recieved by the Google Docs API.
the invoice.


#### Usage
`python docs/create_invoice.py`


