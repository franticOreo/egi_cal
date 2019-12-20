from __future__ import print_function
import datetime
from datetime import datetime
# from datetime import date
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import pprint

# from datetime import datetime, time, date

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def date_and_time(iso_date): 
    # get date and time from ISO format, strip off time zone
    return datetime.strptime(iso_date.split('+')[0], "%Y-%m-%dT%H:%M:%S")
 


def hours_worked(start_time, end_time): 
    # get dates in ISO format and compute the difference in time
    time_diff = end_time - start_time
    return time_diff.total_seconds() / 60 / 60


def cal_events():

    """
    Uses the Google Calendar API to search for users upcoming events and returns
    a list of lists containing relevant information of the event. Including:
    Customer name, number of hours worked, the date of work. 
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.


    events_info = []

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    ########## CANT GET DATE TIME TO PICKLE?
    # dt_last_exe = datetime.strptime(get_last_exe(), "%d/%m/%Y %H:%M:%S")
    # last_exe = dt_last_exe.isoformat() + 'Z'
    # print(last_exe)

    # ## TEMP until last exe fn fixed
    last_exe = datetime(2019, 12, 7).isoformat() + 'Z' 

    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # set date to 2016
    # now = datetime.datetime(2016, 1, 1, 16, 30).isoformat() + 'Z'
    print(now)
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=last_exe,
                                        timeMax=now, maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:

        # edge case for event that does not contain a start time, skip this event
        # if len(event['start']) < 2:
        #     continue
        # get all calendar entries for Work

        if event['summary'].startswith('Work for'):
            events_info.append(relevant_event_info(event))
            print('Found work entry: ', event['summary'])
            print('Extracted info: ', relevant_event_info(event))
            print()

    return events_info

def get_last_exe():
    with open('/home/franticoreo/egi_cal/last_exe.pickle', 'rb') as file:
        last_exe = pickle.load(file)
    return last_exe





def relevant_event_info(event):
    # events_info = []
    # get length of work
    start_time = date_and_time(event['start']['dateTime'])
    end_time = date_and_time(event['end']['dateTime'])

    
    no_of_hours = hours_worked(start_time, end_time)
    name_of_cust = event['summary'].split('Work for')[1]
    date_of_work = date_and_time(event['start']['dateTime']).date()

    event_info = [name_of_cust, no_of_hours, date_of_work]
    # pprint.pprint(event_info)
    # events_info.append(event_info)

    return event_info



if __name__ == '__main__':
    cal_events()



