import json

import spotipy
from spotipy.oauth2 import SpotifyOAuth


# to support Client Authorization Code Flow, SpotifyOAuth is used to authenticate these requests,

class TrackSongs:
    # auth using auth_manager=SpotifyOAuth()
    def __init__(self, client_id, client_secret, redirect_url, scope, limit=25):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_url = redirect_url
        self.scope = scope
        self.limit = limit
        self.sp = None
        self.recent_tracks = None

    def authenticate_user(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id,
                                                            client_secret=self.client_secret,
                                                            redirect_uri=self.redirect_url,
                                                            scope=self.scope))

    def get_recently_played_track_details(self):
        if self.sp is None:
            raise Exception("User not authenticated, call authenticate_user() method first.")

        self.recent_tracks = self.sp.current_user_recently_played(limit=self.limit)
        return self.recent_tracks

    def get_genres_for_artist(self, artist_id):
        artist = self.sp.artist(artist_id)
        return artist['genres']

    def print_recently_played_track(self):
        if self.recent_tracks is None:
            raise Exception("No recently played tracks found, call get_recently_played_track_details() method first.")

        for idx, item in enumerate(self.recent_tracks['items']):
            track = item['track']['name']
            print(f"Track Played: {track}")

    def print_recently_played_track_artist(self):
        if self.recent_tracks is None:
            raise Exception("No recently played tracks found, call get_recently_played_track_details()")

        for idx, item in enumerate(self.recent_tracks['items']):
            artist = item['track']['artists'][0]['name']
            print(f"Artist: {artist}")

    def print_recently_played_track_album(self):
        if self.recent_tracks is None:
            raise Exception("No recently played tracks found, call get_recently_played_track_details()")

        for idx, item in enumerate(self.recent_tracks['items']):
            album = item['track']['album']['name']
            print(f"Album: {album}")

    def print_recently_played_track_album_art(self):
        if self.recent_tracks is None:
            raise Exception("No recently played tracks found, call get_recently_played_track_details()")

        for idx, item in enumerate(self.recent_tracks['items']):
            album_art = item['track']['album']['images'][0]
            print(f"Album Art: {album_art}")

    def print_recently_played_track_song_duration(self):
        if self.recent_tracks is None:
            raise Exception("No recently played tracks found, call get_recently_played_track_details()")

        for idx, item in enumerate(self.recent_tracks['items']):
            song_duration = item['track']['duration_ms']
            print(f"Song Duration in MS: {song_duration}")

    def print_recently_played_track_time_listened(self):
        if self.recent_tracks is None:
            raise Exception("No recently played tracks found, call get_recently_played_track_details()")

        for idx, item in enumerate(self.recent_tracks['items']):
            played_at = item['played_at']
            print(f"Time/date song was played: {played_at}")

    def print_recently_played_track_genre(self):
        if self.recent_tracks is None:
            raise Exception("No recently played tracks found, call get_recently_played_track_details()")

        for idx, item in enumerate(self.recent_tracks['items']):
            artist_id = item['track']['artists'][0]['id']
            genres = self.get_genres_for_artist(artist_id)
            genres_str = ', '.join(genres)
            print(f"Genre of artist: {genres_str}")

    def print_json_response(self):
        if self.recent_tracks is None:
            raise Exception("No recently played tracks found, call get_recently_played_track_details() method first.")

        print(json.dumps(self.recent_tracks, indent=4))
