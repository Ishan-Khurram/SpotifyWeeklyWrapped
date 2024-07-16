import datetime
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build


class SheetsData:

    # Initialize the skeleton so I can import all the needed data into main.py
    def __init__(self, song, artist, album, album_art, genre, song_duration, time_listened, scopes,
                 service_account_file, spreadsheet_id, sheets_range):
        self.song = song
        self.artist = artist
        self.album = album
        self.album_art = album_art
        self.genre = genre
        self.song_duration = song_duration
        self.time_listened = time_listened
        self.spreadsheet_id = spreadsheet_id
        self.service_account_file = service_account_file
        self.scopes = scopes
        self.range = sheets_range

    def authenticate_sheets(self):  # dont know how this works at all. Got this from quick start guide
        """Authenticate and return the Google Sheets service."""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.service_account_file, scopes=self.scopes)
            service = build('sheets', 'v4', credentials=credentials)
            return service.spreadsheets()
        except Exception as e:
            logging.error(f"Failed to authenticate sheets: {e}")
            raise

    def get_recently_listened_to_time(self):
        # Get spreadsheet data, only the last row's recently listened to time
        try:
            sheets = self.authenticate_sheets()
            result = sheets.values().get(spreadsheetId=self.spreadsheet_id, range=self.range).execute()
            values = result.get('values', [])  # parsing the json data and getting needed info
            if not values:
                logging.info("No data found in the specified range.")
                return None
            last_time = values[-1][-1]
            print(f"Last time listened: {last_time}")
            return last_time
        except Exception as e:
            logging.error(f"Failed to fetch recently listened to time: {e}")
            raise

    def append_values(self, authenticated_sheet):
        """Update values in the Google Sheet."""
        # Prepare the data to be input
        try:
            song = self.song
            artist = self.artist
            album = self.album
            album_art = self.album_art
            genre = self.genre
            song_duration = self.song_duration
            time_listened = self.time_listened

            # Define the range and values to be updated
            range_ = self.range  # Use the range provided during initialization
            values = [[song, artist, album, album_art, genre, song_duration, time_listened]]

            body = {
                'values': values  # why is this needed?
            }

            # Send the request to update the values
            result = authenticated_sheet.values().append(
                spreadsheetId=self.spreadsheet_id, range=range_,
                valueInputOption='RAW', body=body).execute()

            print(f"{result.get('updates').get('updatedCells')} cells updated.")
        except Exception as e:
            logging.error(f"Failed to append values: {e}")
            raise
