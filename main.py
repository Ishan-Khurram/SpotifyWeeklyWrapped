from track_songs import TrackSongs
from sheets_data import SheetsData


def main():
    # Data needed for the TrackSongs class
    client_id = '33d00bfd9ac543cd95cd347eba9c8207'
    client_secret = '87339e3f952d41448e8b223c0d80a0a1'
    redirect_url = 'http://localhost:3000'
    scope = "user-read-recently-played"
    limit = 1

    # Initialize TrackSongs Class
    track_songs = TrackSongs(client_id, client_secret, redirect_url, scope, limit)
    track_songs.authenticate_user()
    track_songs.get_recently_played_track_details()

    # Extract track details for readability
    track_details = {
        "track": track_songs.print_recently_played_track(),
        "artist": track_songs.print_recently_played_track_artist(),
        "album": track_songs.print_recently_played_track_album(),
        "album_art": track_songs.print_recently_played_track_album_art(),
        "genre": track_songs.print_recently_played_track_genre(),
        "duration": track_songs.print_recently_played_track_song_duration(),
        "time_listened": track_songs.print_recently_played_track_time_listened()
    }

    # Data needed for the SheetsData Class
    sheety_endpoint = "https://api.sheety.co/b23eae0f5883f25642e9f897747056a0/vibify/main"
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


if __name__ == "__main__":
    main()
