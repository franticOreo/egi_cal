"""
Connect Calendar list of events and search 
sqlite3 database for customers information
"""
import sys
import sqlite3
from sqlite3 import Error
from google_cal import cal_events

sys.path.insert(1, '/home/franticoreo/egi_cal/sqlite')
from insert_data import create_customer


    
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn

'''
Function taken from sqlite3 docs to retain columns from cursor response
in a dictionary form
'''

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_customer_info(conn, customer_name):
    """

    """
    try:
        conn.row_factory = dict_factory
        cur = conn.cursor()
        statement = "SELECT * FROM customers WHERE name LIKE '{}%'".format(customer_name)
        cur.execute(statement)   
        customer_dict = cur.fetchone()
        print(customer_dict)
        return customer_dict

    except Error as e:
        print(e)


def get_event_and_info():
    """
    This function calls cal events and recieves a list of upcoming
    Work calendar events. It creates a connection to the database. It extracts
    customer name from the event and uses customer name to query the DB. The function
    returns a list of lists containing the Event info paired with Customer DB info.
    """
    database = r"/home/franticoreo/egi_cal/sqlite/db/egi_db.db"
    # get upcoming events from google calendar API in a list
    list_of_cust_dicts = []

    upcoming_events = cal_events()
    # create a database connection
    for event in upcoming_events:
        print("Trying to find database entry for event :", event)
        conn = create_connection(database)
        # cur = conn.cursor()
        with conn:
            # get customer name from the event list
            # strip customer name
            customer_name = event[0].strip()
            cust_dict = get_customer_info(conn, customer_name)  
            print(cust_dict)      
            if cust_dict == None:
                cust_dict = {}
                print('Customer: {} not Found!'.format(customer_name))
                # if customer is not found, create a entry 
                # ask user for address, suburb and rate
                # send the hours name, hours worked, date to invoice
                address = input('What is the address for {}:  '.format(customer_name))
                suburb = input('What is the suburb for {}:  '.format(customer_name))
                rate =  input('What is the rate for {}:  '.format(customer_name))
                email = input('What is the email for {}:  '.format(customer_name))   
                # create sqlite db entry for customer
                create_customer(conn, (customer_name, address, suburb, rate, email))

                
                cust_dict['name'] = customer_name
                cust_dict['address'] = address
                cust_dict['suburb'] = suburb  
                cust_dict['rate'] = rate
                cust_dict['email'] = email
                cust_dict['hours-worked'] = event[1]
                cust_dict['date-of-work'] = event[2]
                list_of_cust_dicts.append(cust_dict)
            else:
                print('Customer Found...')
                cust_dict['hours-worked'] = event[1]
                cust_dict['date-of-work'] = event[2]
                list_of_cust_dicts.append(cust_dict)


    return list_of_cust_dicts

 
if __name__ == '__main__':
    print()
    print('Customer and Event info found!: ', get_event_and_info())


# 

# Getting the upcoming 10 events
# [' Noreen', 4.0, datetime.date(2019, 10, 29)]
# [' Jan Applecross', 6.0, datetime.date(2019, 11, 11)]
# [' Jan Lewis', 4.0, datetime.date(2019, 12, 9)]
# 2. Query all tasks
# Traceback (most recent call last):
#   File "conn_cal_db.py", line 61, in <module>
#     main()
#   File "conn_cal_db.py", line 53, in main
#     if select_all_tasks(conn) == None:
#   File "conn_cal_db.py", line 38, in select_all_tasks
#     cur.execute(statement)
# sqlite3.OperationalError: near "Lewis": syntax error

