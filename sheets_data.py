import requests


class SheetsData:

    # initialize the skeleton so i can import all the needed data into main.py
    def __init__(self, song, artist, album, album_art, genre, song_duration, time_listened):
        self.song = song
        self.artist = artist
        self.album = album
        self.album_art = album_art
        self.genre = genre
        self.song_duration = song_duration
        self.time_listened = time_listened
        self.endpoint = None

    def api_info(self, endpoint):
        self.endpoint = endpoint

    def get_recently_listened_time(self):
        if not self.endpoint:
            return False, "Endpoint not specified, use api_info() method to continue."

        response = requests.get(url=self.endpoint)

        data = response.json()

        # print("response.status_code =", response.status_code)
        # print("response.text= ", response.text)

        last_element = data['main'][-1]
        time_listened = last_element['timeListened']
        return time_listened

    def push_data_to_spreadsheet(self):
        if not self.endpoint:
            return False, "Endpoint not specified, use api_info() method to continue."

        # title names for sheet columns MUST be camelCased when using them here
        # or the data won't be posted
        data = {
            "main": {
                "song": self.song,
                "artist": self.artist,
                "album": self.album,
                "albumArt": self.album_art,
                "genre": self.genre,
                "songDuration": self.song_duration,
                "timeListened": self.time_listened,
            }
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url=self.endpoint, json=data, headers=headers)

        if response.status_code == 200:
            return True, print("Data successfully pushed to the spreadsheet")
        else:
            return False, print(f"Failed to push data. Status code: {response.status_code}, Response: {response.text}")
