from __future__ import print_function
import pickle
import os.path
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from google.oauth2 import service_account

import sys
# relative import 
sys.path.insert(1, '/home/franticoreo/egi_cal')
from conn_cal_db import get_event_and_info

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly', 
'https://www.googleapis.com/auth/drive']

# The ID of a sample document.
DOCUMENT_ID = '1c3dW6AfZv__YJNcvqicRPffCebgvBuhoW93GhCaHYwY'




def input_invoice_data(cust_dict, title):
    """
    Creates a Google Doc Invoice with the Google Docs API.
    """

    invoice_copy_id, creds = create_new_invoice(title)
    doc_service = build('docs', 'v1', credentials=creds)
    # Retrieve the documents contents from the Docs service.
    document = doc_service.documents().get(documentId=invoice_copy_id).execute()
    requests = arrange_requests(cust_dict)
    
    result = doc_service.documents().batchUpdate(
        documentId=invoice_copy_id, body={'requests': requests}).execute()



def get_expenses(cust_dict):
    """Asks user for quantity, type of expense and cost. It adds these
    to the customer dictionary.
    Ask user if expenses, if so ask for data else break.
    """
    more_expenses = True
    count = 0

    while more_expenses==True:
        are_there = input('Are there any expenses for the job: {} on the {}? y/N'.format(cust_dict['name'], cust_dict["date-of-work"]))
# NEEEEEEEEEEEEEEDS WORK

        if are_there == 'y':
            key = 'expense' + str(count)
            cust_dict[key] = input()
        if are_there == 'N':
            more_expenses = False




def arrange_requests(cust_dict):
    """
    Creates a request object in JSON form for the Google Docs API
    """
    expenses = get_expenses(cust_dict)

    inv_num = title.split('-')[0]
    print(cust_dict['hours-worked'], cust_dict['email'] )
    labour_cost = str(int(cust_dict['hours-worked']) * int(cust_dict['rate']))

    requests = [
         {
            'replaceAllText': {
                'containsText': {
                    'text': '{{date-of-work}}',
                    'matchCase':  'true'
                },
                'replaceText': cust_dict['date-of-work'].strftime("%d-%m-%Y"),
            }}, {
            'replaceAllText': {
                'containsText': {
                    'text': '{{tax-invoice-number}}',
                    'matchCase':  'true'
                },
                'replaceText': inv_num,
            }}, {
            'replaceAllText': {
                'containsText': {
                    'text': '{{name}}',
                    'matchCase':  'true'
                },
                'replaceText': cust_dict['name'],
            }
        }, {
            'replaceAllText': {
                'containsText': {
                    'text': '{{address}}',
                    'matchCase':  'true'
                },
                'replaceText': cust_dict['address'],
            }
        }, {
            'replaceAllText': {
                'containsText': {
                    'text': '{{suburb}}',
                    'matchCase':  'true'
                },
                'replaceText': cust_dict['suburb'],
            }
        }, {
            'replaceAllText': {
                'containsText': {
                    'text': '{{hours-worked}}',
                    'matchCase':  'true'
                },
                'replaceText': str(cust_dict['hours-worked']),
            }
        }, {
            'replaceAllText': {
                'containsText': {
                    'text': '{{labour-cost}}',
                    'matchCase':  'true'
                },
                'replaceText': labour_cost,
            }
        }
    ]

    return requests

def create_invoice_title(inv_info):
    '''
    Takes the invoice dictionary and creates a unique title, counting
    invoice number
    '''
    num = increment_num()

    title = num + '-' + inv_info['name']+ '-' + 'Gardening' + '-' 
    # convert datetime object to UK/AUS format
    title = title + inv_info['date-of-work'].strftime("%d-%m-%Y") 
    # if a space in title replace with hyphen
    title.replace(' ', '-')

    print(title)
    return title

def increment_num():
    # increment invoice number from txt file
    with open('invoice_number.txt', 'r') as curr_num:
        current_number = curr_num.read()
        print(current_number)
        with open('invoice_number.txt', 'w') as new_num:
            print(current_number)
            new_number = int(current_number) + 1
            new_num.write(str(new_number))
    return current_number
    

def create_new_invoice(title):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('drive_token.pickle'):
        with open('drive_token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'creds_client_config.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('drive_token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    drive_service = build('drive', 'v3', credentials=creds)

    body = {
        'name': title
    }

    new_copy = drive_service.files().copy(
        fileId=DOCUMENT_ID, body=body).execute()
    invoice_copy_id = new_copy.get('id')

    return invoice_copy_id, creds

# DEBUGGING STOLEN FROM STACK OVERFLOW
# import dis
# def list_func_calls(fn):
#     funcs = []
#     bytecode = dis.Bytecode(fn)
#     instrs = list(reversed([instr for instr in bytecode]))
#     for (ix, instr) in enumerate(instrs):
#         if instr.opname=="CALL_FUNCTION":
#             load_func_instr = instrs[ix + instr.arg + 1]
#             funcs.append(load_func_instr.argval)

#     return ["%d. %s" % (ix, funcname) for (ix, funcname) in enumerate(reversed(funcs), 1)]



if __name__ == '__main__':
    '''
    create a invoice for the amount of dictionarys in the in the list
    input the data for each invoice
    '''
    list_cust_dict = get_event_and_info()
    inv_created = []

    for cust_dict in list_cust_dict:
        print("cust_dic", cust_dict)
        title = create_invoice_title(cust_dict)
        inv_created.append(title)
        input_invoice_data(cust_dict, title)

    print()
    print('Completed!')
    print('{}'.format(len(list_cust_dict)) + ' Invoice/s created!')
    user_res = input('Are you satisfied with the result? y/N')

    # Writing the current time to file for next calendar entry request -see ../google_cal.py
    if user_res == 'y' or user_res == 'Y':
        with open('/home/franticoreo/egi_cal/last_exe.pickle', 'wb') as file:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            pickle.dump(now, file)







