import spotipy
from spotipy.oauth2 import SpotifyOAuth


class TrackSongs:
    """
    Class to handle Spotify track operations using Spotipy.
    """

    def __init__(self, client_id, client_secret, redirect_url, scope, limit):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_url = redirect_url
        self.scope = scope
        self.limit = limit
        self.sp = None
        self.recent_tracks = None
        self.username = "ishan_khurram"

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

    def get_recent_track_detail(self, detail):
        if self.recent_tracks is None:
            raise Exception("No recently played tracks found, call get_recently_played_track_details() method first.")

        for item in self.recent_tracks['items']:
            track = item['track']
            if detail == "track":
                return track['name']
            elif detail == "artist":
                return track['artists'][0]['name']
            elif detail == "album":
                return track['album']['name']
            elif detail == "album_art":
                return track['album']['images'][0]["url"]
            elif detail == "song_duration":
                return track['duration_ms']
            elif detail == "played_at":
                return item['played_at']
            elif detail == "genre":
                artist_id = track['artists'][0]['id']
                genres = self.get_genres_for_artist(artist_id)
                return ', '.join(genres)

    def print_recently_played_track(self):
        return self.get_recent_track_detail("track")

    def print_recently_played_track_artist(self):
        return self.get_recent_track_detail("artist")

    def print_recently_played_track_album(self):
        return self.get_recent_track_detail("album")

    def print_recently_played_track_album_art(self):
        return self.get_recent_track_detail("album_art")

    def print_recently_played_track_song_duration(self):
        return self.get_recent_track_detail("song_duration")

    def print_recently_played_track_time_listened(self):
        return self.get_recent_track_detail("played_at")

    def print_recently_played_track_genre(self):
        return self.get_recent_track_detail("genre")

    def add_tracks_to_playlist(self, playlist_id, track_ids):
        self.sp.playlist_add_items(playlist_id, track_ids)

    def get_recently_played_tracks(self, limit=50):
        if self.sp is None:
            raise Exception("User not authenticated, call authenticate_user() method first.")
        return self.sp.current_user_recently_played(limit=limit)['items']

    def get_recommendations(self, seed_tracks, limit=30):
        return self.sp.recommendations(seed_tracks=seed_tracks, limit=limit)['tracks']

    def create_playlist(self, name1, public=True):
        playlist = self.sp.user_playlist_create(user=self.username, name=name1, public=public)
        return playlist['id']

    def melodys_playlist(self, playlist_name="Melody's Playlist"):
        if self.sp is None:
            raise Exception("User not authenticated, call authenticate_user() method first.")

        # Get the user's recently played tracks
        recently_played = self.get_recently_played_tracks(limit=50)

        # Extract track IDs from the recently played tracks
        track_ids = [item['track']['id'] for item in recently_played]

        # Generate recommendations based on the recently played tracks
        recommendations = self.get_recommendations(seed_tracks=track_ids[:5], limit=50)

        # Extract recommended track IDs
        recommended_track_ids = [track['id'] for track in recommendations]

        # Create a new playlist
        playlist_id = self.create_playlist(name1=playlist_name, public=True)

        # Add recommended tracks to the new playlist
        self.add_tracks_to_playlist(playlist_id=playlist_id, track_ids=recommended_track_ids)

        print(f"Playlist '{playlist_name}' created successfully with {len(recommended_track_ids)} tracks!")

