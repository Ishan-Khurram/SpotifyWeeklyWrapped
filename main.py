from track_songs import TrackSongs
from sheets_data import SheetsData
import time


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

    while True:
        try:
            # Initialize SheetsData class with dummy values
            sheets_data = SheetsData("", "", "", "", "", "", "")
            sheety_endpoint = "https://api.sheety.co/b23eae0f5883f25642e9f897747056a0/vibify/main"
            sheets_data.api_info(endpoint=sheety_endpoint)

            # Get the last time listened from the Google Sheet
            last_time_listened = sheets_data.get_recently_listened_time()

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

            # Check if the time listened is different before updating
            if track_details["time_listened"] != last_time_listened:
                print("New track detected, updating spreadsheet.")  # Debugging output

                # Initialize SheetsData class with actual track details
                sheets_data = SheetsData(
                    track_details["track"],
                    track_details["artist"],
                    track_details["album"],
                    track_details["album_art"],
                    track_details["genre"],
                    track_details["duration"],
                    track_details["time_listened"]
                )
                sheets_data.api_info(endpoint=sheety_endpoint)

                # Post data to the spreadsheet
                sheets_data.push_data_to_spreadsheet()
            else:
                print("No new track, no update needed.")  # Debugging output

        except Exception as e:
            print("An error occurred:", e)  # Debugging output

        # Sleep for 30 seconds before checking again
            """
            This will eventually be replaced with a yml (YAML) file 
            to allow for periodic checking.
            """
        time.sleep(5)

        """
        
        """


if __name__ == "__main__":
    main()
