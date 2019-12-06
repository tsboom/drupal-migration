from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pdb

# # If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of spreadsheet.
SPREADSHEET_ID = '15eXz2MMLhm-I1e_pcpfW6ct-BT6g9l3HgV-OYRS100I'

# real range
CONTENT_RANGE = 'Content Inventory!C2:U2779'

# big chunk of archive pages test
#CONTENT_RANGE = 'Content Inventory!C1245:U2560'
# CONTENT_RANGE = 'Content Inventory!C2322:U2560'


def authenticate_gsheet():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
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
            # credentials_path = os.path.abspath('credentials.json')
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service


def get_content_audit_values():
    service = authenticate_gsheet()
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=CONTENT_RANGE).execute()
    values = result.get('values', [])
    return values
    
    
    
if __name__ == '__main__':
    main()
