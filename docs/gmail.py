from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_cust_emails():
    """Gets customer emails

    Returns:
        A unique list of dictionaries, containing subject line & recip
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'gmail_creds.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    msgs = ListMessagesMatchingQuery(service, 'me', query='Tax Invoice')
    # print(msgs)
    s = "Reading {} Emails...".format(len(msgs))
    print(s)
    subj_and_recip = []
    for msg in msgs:
        email_resources = service.users().messages().get(userId='me', id=msg['id']).execute()
        # print(msg['snippet'])
        email_d = {}
        for resource in email_resources['payload']['headers']:
            if resource['name'] == 'To':
                # to = resource['value']
                # subj_and_recip.append(subj)
                email_d['recip'] = resource['value']
            if resource['name'] == 'Subject':
                # get the emails subject line
                # subj = resource['value']
                # subj_and_recip.append(subj)
                email_d['subj'] = resource['value']
            subj_and_recip.append(email_d)
    # print(subj_and_recip)

    unique_entries = [dict(t) for t in {tuple(d.items()) for d in subj_and_recip}]    

    eli = 'Eli Simic <eli.simic.robertson@gmail.com>'

    # remove_eli = [d for d in unique_entries if d['recip'] != eli]
    clean_entries = []
    for d in unique_entries:
        # remove entries without both recipient & subject line
        if len(d) < 2:
            continue
        print(d)
        # if recipient is Eli Simic ... skip the dictionary
        if d['recip'] == eli:
            continue
        # remove cases where dictionary is part of reply thread
        if d['subj'].startswith('RE') or d['subj'].startswith('Re'):
            continue

        else:
        # add 
            clean_entries.append(d)
    
    with open('clean_entries_no_gc.txt', 'wb') as file:
        pickle.dump(clean_entries, file)
    print(clean_entries)
    return clean_entries



"""Get a list of Messages from the user's mailbox.
"""

from apiclient import errors


def ListMessagesMatchingQuery(service, user_id, query=''):
    try:
        response = service.users().messages().list(userId=user_id,
                       q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query,
                                             pageToken=page_token).execute()
            messages.extend(response['messages'])

            return messages
    except errors.HttpError:
        print('An error occurred: {}').format(errors.HttpError) 








if __name__ == '__main__':
    get_cust_emails()