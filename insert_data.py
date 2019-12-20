import sqlite3
from sqlite3 import Error
from get_invoices_data import get_cust_info, clean_cust_info


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn
 
 
def create_customer(conn, project):
    """
    """
    sql = ''' INSERT INTO customers(name, email, address, suburb, rate)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid
 
 
 
def main():
    list_of_cust = get_cust_info()
    unique_cust = clean_cust_info(list_of_cust)

    database = r"/home/franticoreo/egi_cal/db/egi_db.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        for customer in unique_cust:
            # create a new project
            # project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
            project_id = create_customer(conn, customer)

 
if __name__ == '__main__':
    main()