from __future__ import print_function
import json
import base64
from jira import JIRA
import re
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

JIRA_CONFIG_FILE = '../jira_config.json'
JIRA_SERVER_OPTIONS = 'jira_server_options'
JIRA_USR = 'jira_usr'
JIRA_PASS = 'jira_pass'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '19E3lnqPh74QkscXkenl4GbevNJiylrrSwoBf0sWWr7s'
SPREADSHEET_RANGE_NAME = 'Class Data!A2:E'

def init_jira_from_json():
    with open(JIRA_CONFIG_FILE, 'r') as json_file:
        json_data = json.load(json_file)

    jira_server_options = json_data[JIRA_SERVER_OPTIONS]
    jira_usr = json_data[JIRA_USR]
    jira_pass = base64.b64decode(json_data[JIRA_PASS]).decode('ascii')
    jira = JIRA(jira_server_options, basic_auth=(jira_usr, jira_pass))

    return jira

def init_google_spreadsheet():
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    return sheet

if __name__ == "__main__":
    jira = init_jira_from_json()
    projects = jira.projects()
    print(projects)

    sheet = init_google_spreadsheet()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=SPREADSHEET_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))