# egi_cal
###### Creates Google Doc Invoices for my business, Eli's Garden Improvements

#### Goal
Automate invoice creation from calendar entry.

#### Methodology
This project reads past Google Calendar entries with the Google Calendar API. This calendar information is then parsed and matched to the relevent customers information to a SQL database (SQLite3). This is combined into a invoice dictionary which is recieved by the Google Docs API.

#### Problems
Difficulty with using Calendar as first point of data entry. If multiple workers are working on a day this is hard to represent this with Google Maps. Additionally, abritrary expenses are difficult to parse into Google Doc.

#### Results
Ensures that invoices and data input is **consistent**(lowers chances of human error). Also, a huge **time saving** in preparing the invoice for basic information, e.g customer address, date of work.  

#### Example Invoice
The final result is a Google Doc filled with relevent customer information, an incremented invoice number, amount of hours worked and cost. The only manual work is to fill in the expenses and total the invoice. **Placeholder values have been used for security reasons**

![example_invoice](/images/invoice_example.png)

#### Usage
`python docs/create_invoice.py`


