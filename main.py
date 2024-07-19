import os
import time
import logging
from track_songs import TrackSongs
from sheets_data import SheetsData

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler(), logging.FileHandler('debug.log')])


def main():
    # Data needed for the TrackSongs class
    client_id = "33d00bfd9ac543cd95cd347eba9c8207"
    client_secret = "87339e3f952d41448e8b223c0d80a0a1"
    redirect_url = 'http://localhost:3000'
    scope = "user-read-recently-played"
    limit = 1

    # Initialize TrackSongs Class
    track_songs = TrackSongs(client_id, client_secret, redirect_url, scope, limit)
    track_songs.authenticate_user()

    # Getting env variables and other variables needed for google sheets API
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = "credentials.json"
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    RANGE = os.getenv("RANGE_NAME")

    while True:
        try:
            # Get last time listened
            sheets_data = SheetsData("", "", "", "", "", "", "", "", SERVICE_ACCOUNT_FILE, SPREADSHEET_ID, RANGE)
            last_time_listened = sheets_data.get_recently_listened_to_time()
            print(last_time_listened)

            # Get all track of last track details
            track_songs.get_recently_played_track_details()

            track_details = {
                "track": track_songs.print_recently_played_track(),
                "artist": track_songs.print_recently_played_track_artist(),
                "album": track_songs.print_recently_played_track_album(),
                "album_art": track_songs.print_recently_played_track_album_art(),
                "genre": track_songs.print_recently_played_track_genre(),
                "duration": track_songs.print_recently_played_track_song_duration(),
                "time_listened": track_songs.print_recently_played_track_time_listened()
            }
            print(track_details["time_listened"])

            # Check if the time listened is different before updating
            if last_time_listened != track_details["time_listened"]:
                logging.info("New track detected, updating spreadsheet.")  # Debugging output

                # Input actual data
                sheets_data = SheetsData(
                    song=track_details["track"],
                    artist=track_details["artist"],
                    album=track_details["album"],
                    album_art=track_details["album_art"],
                    genre=track_details["genre"],
                    song_duration=track_details["duration"],
                    time_listened=track_details["time_listened"],
                    scopes=SCOPES,
                    service_account_file=SERVICE_ACCOUNT_FILE,
                    spreadsheet_id=SPREADSHEET_ID,
                    sheets_range=RANGE
                )

                sheets = sheets_data.authenticate_sheets()

                result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
                values = result.get('values', [])

                if not values:
                    logging.info("No Data Found")
                else:
                    logging.info(f"Last row: {values[-1]}")  # to print last value only
                    sheets_data.append_values(sheets)
            else:
                print("No new track, update not needed.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")  # Debugging output

        # Sleep for 120 seconds before checking again
        time.sleep(120)


if __name__ == "__main__":
    main()
