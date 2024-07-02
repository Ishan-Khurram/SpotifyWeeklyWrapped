from track_songs import TrackSongs


def main():
    client_id = '33d00bfd9ac543cd95cd347eba9c8207'
    client_secret = '87339e3f952d41448e8b223c0d80a0a1'
    redirect_url = 'http://localhost:3000'
    scope = "user-read-recently-played"
    limit = 25

    track_songs = TrackSongs(client_id, client_secret, redirect_url, scope, limit)
    track_songs.authenticate_user()
    track_songs.get_recently_played_track_details()
    # track_songs.print_json_response()  # Print the entire JSON response
    track_songs.print_recently_played_track()


if __name__ == "__main__":
    main()
