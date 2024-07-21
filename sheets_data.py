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
            last_time = values[-1][6]
            return last_time
        except Exception as e:
            logging.error(f"Failed to fetch recently listened to time: {e}")
            raise

    def get_top_album_arts(self):
        # Get spreadsheet data, only the last row's recently listened to time
        try:
            sheets = self.authenticate_sheets()
            result = sheets.values().get(spreadsheetId=self.spreadsheet_id, range="topTracksOfWeek").execute()
            values = result.get('values', [])  # parsing the json data and getting needed info
            if not values:
                logging.info("No data found in the specified range.")
                return None
            top_album_art = []
            counter = 1
            while counter <= 5:
                top_album_art.append(values[counter][-1])
                counter += 1
            return top_album_art
        except Exception as e:
            logging.error(f"Failed to fetch top tracks: {e}")
            raise

    def get_streams_for_top_songs(self):
        # Get spreadsheet data, only the last row's recently listened to time
        try:
            sheets = self.authenticate_sheets()
            result = sheets.values().get(spreadsheetId=self.spreadsheet_id, range="topTracksOfWeek").execute()
            values = result.get('values', [])  # parsing the json data and getting needed info
            if not values:
                logging.info("No data found in the specified range.")
                return None
            top_tracks_streams = []
            counter = 1
            while counter <= 5:
                top_tracks_streams.append(values[counter][3])
                counter += 1
            return top_tracks_streams
        except Exception as e:
            logging.error(f"Failed to fetch top tracks: {e}")
            raise

    def get_top_tracks(self):
        # Get spreadsheet data, only the last row's recently listened to time
        try:
            sheets = self.authenticate_sheets()
            result = sheets.values().get(spreadsheetId=self.spreadsheet_id, range="topTracksOfWeek").execute()
            values = result.get('values', [])  # parsing the json data and getting needed info

            if not values:
                logging.info("No data found in the specified range.")
                return None
            top_songs = []
            counter = 1
            while counter <= 5:
                top_songs.append(values[counter][0])
                counter += 1
            return top_songs
        except Exception as e:
            logging.error(f"Failed to fetch top tracks: {e}")
            raise

    def get_artists_attributed_to_top_tracks(self):
        # Get spreadsheet data, only the last row's recently listened to time
        try:
            sheets = self.authenticate_sheets()
            result = sheets.values().get(spreadsheetId=self.spreadsheet_id, range="topTracksOfWeek").execute()
            values = result.get('values', [])  # parsing the json data and getting needed info

            if not values:
                logging.info("No data found in the specified range.")
                return None
            top_artists_of_tracks = []
            counter = 1
            while counter <= 5:
                top_artists_of_tracks.append(values[counter][1])
                counter += 1
            return top_artists_of_tracks
        except Exception as e:
            logging.error(f"Failed to fetch top tracks: {e}")
            raise

    def get_top_artists(self):
        # Get spreadsheet data, only the last row's recently listened to time
        try:
            sheets = self.authenticate_sheets()
            result = sheets.values().get(spreadsheetId=self.spreadsheet_id, range="topArtistsOfWeek").execute()
            values = result.get('values', [])  # parsing the json data and getting needed info

            if not values:
                logging.info("No data found in the specified range.")
                return None
            top_artists = []
            counter = 1
            while counter <= 5:
                top_artists.append(values[counter][0])
                counter += 1
            return top_artists
        except Exception as e:
            logging.error(f"Failed to fetch top artists: {e}")
            raise

    def get_listening_minutes_per_artist(self):
        # Get spreadsheet data, only the last row's recently listened to time
        try:
            sheets = self.authenticate_sheets()
            result = sheets.values().get(spreadsheetId=self.spreadsheet_id, range="topArtistsOfWeek").execute()
            values = result.get('values', [])  # parsing the json data and getting needed info

            if not values:
                logging.info("No data found in the specified range.")
                return None
            listening_minutes = []
            counter = 1
            while counter <= 5:
                listening_minutes.append(values[counter][1])
                counter += 1
            return listening_minutes
        except Exception as e:
            logging.error(f"Failed to fetch top artists: {e}")
            raise

    def get_top_genres(self):
        # Get spreadsheet data, only the last row's recently listened to time
        try:
            sheets = self.authenticate_sheets()
            result = sheets.values().get(spreadsheetId=self.spreadsheet_id, range="topGenresOfWeek").execute()
            values = result.get('values', [])  # parsing the json data and getting needed info

            if not values:
                logging.info("No data found in the specified range.")
                return None
            top_genres = []
            counter = 1
            while counter <= 3:
                top_genres.append(values[counter][0])
                counter += 1
            return top_genres
        except Exception as e:
            logging.error(f"Failed to fetch top Genres: {e}")
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

            # Check if the genre needs to be replaced
            if genre == "gen z singer-songwriter":
                genre = "New Gen Classic/Jazz"

            # Define the range and values to be updated
            range_ = self.range  # Use the range provided during initialization
            values = [[song, artist, album, album_art, genre, song_duration, time_listened]]

            body = {
                'values': values
            }

            # Send the request to update the values
            result = authenticated_sheet.values().append(
                spreadsheetId=self.spreadsheet_id, range=range_,
                valueInputOption='USER_ENTERED', body=body).execute()

            print(f"{result.get('updates').get('updatedCells')} cells updated.")
        except Exception as e:
            logging.error(f"Failed to append values: {e}")
            raise
