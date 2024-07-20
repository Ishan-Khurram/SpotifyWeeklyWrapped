import os
import time
import logging
from track_songs import TrackSongs
from sheets_data import SheetsData
import datetime
from gemini_ai import Gemini

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler(), logging.FileHandler('debug.log')])


def main():
    # Data needed for the TrackSongs class
    client_id = "33d00bfd9ac543cd95cd347eba9c8207"
    # Rotated Client Secret
    client_secret = os.getenv("SPOTIFY_SECRET")
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

    # init sheets_data
    sheets_data = SheetsData("", "", "", "", "", "", "", "", SERVICE_ACCOUNT_FILE, SPREADSHEET_ID, RANGE)

    # initialize all things Gemini.
    top5_tracks = sheets_data.get_top_tracks()
    top5_streams = sheets_data.get_streams_for_top_songs()
    top5_album_arts = sheets_data.get_top_album_arts()
    top5_artists = sheets_data.get_top_artists()
    top5_listening_minutes_per_artist = sheets_data.get_listening_minutes_per_artist()
    top_genres = sheets_data.get_top_genres()

    prompt = (f"You are an Upbeat Music assistant, who is happy to be helping curate and analyze Ishan's listening "
              f"data. Start off with saying your name is Melody, and that you are Ishan's personal music assistant. "
              f"Generate"
              f"a personalized email summarizing Ishan's recent listening habits. Include a brief overview of "
              f"listening trends, a section for top tracks: {top5_tracks} with album art links: {top5_album_arts} and "
              f"streams: {top5_streams}, a section for top artists: {top5_artists} with listening time: "
              f"{top5_listening_minutes_per_artist}, and a section for top genres: {top_genres}. Provide at least "
              f"three artist recommendations for each of the user's top five artists Give this its own section. Also "
              f"jot down a very small sentence on what the vibe of the artist or band you are reccomending is like. "
              f"Conclude with a message about"
              f"creating a new playlist named Melody's Mix for Ishan and that it is in his library. Sign off as "
              f"Melody.")

    gemini = Gemini()
    gemini.generate_response(prompt)

    today = datetime.datetime.now()

    if today.weekday() == 5:  # 4 means friday
        response = gemini.generate_response(prompt)
        print(response)
    else:
        pass

    while True:
        try:
            # Get last time listened
            last_time_listened = sheets_data.get_recently_listened_to_time()
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
