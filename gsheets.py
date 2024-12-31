'''.
Google sheets service class
'''

from os import path, getenv
import sys
from dotenv import load_dotenv

from utils import throw_error

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# The ID and range of a sample spreadsheet.
SAMPLE_RANGE_NAME = "Class Data!A2:E"

class GSheets:
    '''
    Google sheets class
    '''
    def __init__(self):
        # Load and validate env variables
        load_dotenv()

        self.credentials_path = getenv('GAPP_CREDENTIALS')
        self.sheet_id = getenv('SHEET_ID')
        self.sheet_name = getenv('SHEET_NAME')

        if not self.sheet_name:
            self.sheet_name = 'Expenses' # Set default

        if not self.credentials_path or not self.sheet_id:
            throw_error('Please make sure the envs GAPP_CREDENTIALS and SHEET_ID are set.')

        # Set readonly fields
        self.scopes = ["https://www.googleapis.com/auth/spreadsheets"]

        # This is for the OAuth token credentials
        self.creds = None

    def __load_credentials(self):
        '''
        Checks for valid OAuth token credentials
        in case there are none, the user has to login
        again.
        '''

        # When a token exists, try to load the credentials from there
        if path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file("token.json", self.scopes)

        # If there are no credentials or they expired, the user has to login again
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scopes
                )
                creds = flow.run_local_server(port=0)

                with open('token.json', 'w', encoding='utf-8') as token:
                    token.write(creds.to_json())

                # Retry the auth
                self.creds = Credentials.from_authorized_user_file("token.json", self.scopes)

    def add_expense(self, expenses):
        '''
        Adds an expense to the expense table
        in the corresponding spreadsheet's table
        '''
        self.__load_credentials()

        try:
            service = build("sheets", "v4", credentials=self.creds)

            # Specify the range and prepare the data to append
            range_name = f"{self.sheet_name}!A:E" # We want the columns A to E from the table
            body = { 'values': expenses }

            # Call the Sheets API to append the data
            sheet = service.spreadsheets()
            result = (
                sheet.values().append(
                    spreadsheetId=self.sheet_id,
                    range=range_name,
                    valueInputOption="USER_ENTERED",
                    body=body
                ).execute()
            )

            print(f"Expenses inserted: {result.get('updates').get('updatedRange')}")

        except HttpError as err:
            throw_error(f"Failed to add expense: {err}")
