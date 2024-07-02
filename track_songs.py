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
            artist = item['track']['artists'][0]['name']
            album = item['track']['album']['name']
            album_art = item['track']['album']['images'][0]
            song_duration = item['track']['duration_ms']
            played_at = item['played_at']
            artist_id = item['track']['artists'][0]['id']
            genres = self.get_genres_for_artist(artist_id)
            genres_str = ', '.join(genres)
            print(
                f"{idx + 1}. Track: {track} // Artist: {artist}// Album: {album}// time played:({played_at}) // album "
                f"art: {album_art} // duration (ms): {song_duration} // Genre of Artist: {genres_str}")

    def print_json_response(self):
        if self.recent_tracks is None:
            raise Exception("No recently played tracks found, call get_recently_played_track_details() method first.")

        print(json.dumps(self.recent_tracks, indent=4))
