import os
import time
import logging
import json
from track_songs import TrackSongs
from sheets_data import SheetsData
import datetime
from gemini_ai import Gemini

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler(), logging.FileHandler('debug.log')])


# Helper function to format the email content
def format_email_content(filtered_intro, top5_tracks, artists_attributed_to_top_tracks, top5_streams, top5_album_arts,
                         top5_artists,
                         top5_listening_minutes_per_artist, top_genres, recommendations):
    recommendations_html = ""
    for rec in recommendations['recommendations']:
        recommendations_html += f'<h2>{rec["artist"]}</h2>'
        for similar_artist in rec['similar_artists']:
            recommendations_html += f'<p><strong>{similar_artist["name"]}</strong> - {similar_artist["blurb"]}</p>'

    # Helper function to format the email header

    return f"""
    <html>
    <head>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                color: #333333;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
            }}
            .container {{
                width: 90%;
                max-width: 600px;
                margin: 20px auto;
                padding: 20px;
                background-color: #ffffff;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
            }}
            h1 {{
                font-size: 24px;
                font-weight: bold;
                text-align: center;
                margin-bottom: 20px;
            }}
            h2 {{
                font-size: 20px;
                font-weight: bold;
                text-decoration: underline;
                margin-top: 20px;
            }}
            h3 {{
                font-size: 18px;
                font-weight: bold;
                text-align: center;
                margin-top: 10px;
            }}
            p {{
                margin-left: 20px;
            }}
            .track {{
                margin-left: 20px;
            }}
            .track img {{
                max-width: 100px;
                display: block;
            }}
            .recommendations {{
                margin-left: 20px;
                line-height: 1.6;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Your Weekly Listening Report</h1>
            <h3>Curated by Melody, Your Personal Musical Assistant.</h3>
        </div>
        <hr>
        <div class="container">
            <h1>Hey Ishan!</h1>
            <h4>{filtered_intro}</h4>
            <h2>Your Top Tracks This Week</h2>
            {''.join([f'<div class="track"><p><strong>{i + 1}. {track}</strong> by {artist} [Streams: {stream}]</p><img src="{album_art}" alt="Album Art"></div>' for i, (track, artist, stream, album_art) in enumerate(zip(top5_tracks, artists_attributed_to_top_tracks, top5_streams, top5_album_arts))])}
            <h2>Your Top Artists This Week</h2>
            {''.join([f'<p>{i + 1}. {artist} ({minutes} minutes)</p>' for i, (artist, minutes) in enumerate(zip(top5_artists, top5_listening_minutes_per_artist))])}
            <h2>Your Top Genres This Week</h2>
            <p>{', '.join(top_genres)}</p>
            <h2>Artist Recommendations</h2>
            <div class="recommendations">{recommendations_html}</div> <h2>New Playlist For You!</h2> <h4>I've 
            carefully woven together a symphony of your sonic preferences into a playlist I call "Your Tune, 
            My Melody." It's a harmonious blend of your favorite notes, crafted with care to create a soundtrack that 
            resonates with your soul. I've added it to your Spotify library, so you can find it anytime you want to 
            escape into your own personal soundscape.</p> <p>Happy listening!</h4> <h4>Melody</h4> </div> </body> 
            </html>"""


def main():
    client_id = "33d00bfd9ac543cd95cd347eba9c8207"
    client_secret = os.getenv("SPOTIFY_SECRET")
    redirect_url = 'http://localhost:3000'
    scope = 'user-library-read playlist-modify-public user-top-read user-read-recently-played'
    limit = 1

    track_songs = TrackSongs(client_id, client_secret, redirect_url, scope, limit)
    track_songs.authenticate_user()

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = "credentials.json"
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
    RANGE = os.getenv("RANGE_NAME")

    sheets_data = SheetsData("", "", "", "", "", "", "", "", SERVICE_ACCOUNT_FILE, SPREADSHEET_ID, RANGE)

    top5_tracks = sheets_data.get_top_tracks()
    artists_attributed_to_top_tracks = sheets_data.get_artists_attributed_to_top_tracks()
    top5_streams = sheets_data.get_streams_for_top_songs()
    top5_album_arts = sheets_data.get_top_album_arts()
    top5_artists = sheets_data.get_top_artists()
    top5_listening_minutes_per_artist = sheets_data.get_listening_minutes_per_artist()
    top_genres = sheets_data.get_top_genres()

    prompt = (f"You are an Upbeat Music assistant, who is happy to be helping curate and analyze Ishan's listening "
              f"data. Start off with saying your name is Melody, and that you are Ishan's personal music assistant. "
              f"Generate a personalized email summarizing Ishan's recent listening habits. Include a brief overview of "
              f"listening trends and start the email with a small paragraph on how this week's listening has been like. "
              f"Include a section for top tracks: {top5_tracks} with album art links: {top5_album_arts} and streams: {top5_streams} "
              f"as well as the artists attributed to the top 5 tracks: {artists_attributed_to_top_tracks}. "
              f"Include a section for top artists: {top5_artists} with listening time: {top5_listening_minutes_per_artist}, "
              f"and a section for top genres: {top_genres}."
              f"Conclude with a message about creating a new playlist named Melody's Mix for Ishan and that it is in "
              f"his library."
              f"Sign off as Melody.")

    prompt_for_recommended_artists = (f"Given the following top 5 artists for the week, recommend 3 similar artists "
                                      f"for each and include a song by each recommended artist along with a short "
                                      f"blurb explaining why I might like them. My top 5 Artists for the week are: "
                                      f"{top5_artists} Output all this data into a JSON format so that Ishan can "
                                      f"easily parse through it.")

    prompt_for_intro = {
        f"Your name is Melody, and you are my personal music assistant. Given these Genres: {top_genres}, i want you to respond with a hearty hello, and talk about my music habits for the week, before saying that we are going to be 'diving into the analytics.'"}

    gemini = Gemini()
    response_dict = gemini.generate_and_extract(prompt)

    # intro
    intro = gemini.generate_and_extract(prompt_for_intro)
    filtered_intro = intro["candidates"][0]["content"]["parts"][0]["text"]

    last_sent_date = None

    while True:
        try:
            today = datetime.date.today()
            if today.weekday() == 2 and (
                    last_sent_date is None or last_sent_date != today):  # 2 indicates Thursday
                email_text = response_dict["candidates"][0]["content"]["parts"][0]["text"]

                subject, body = email_text.split("\n", 1)
                subject = subject.replace("Subject: ", "").strip()

                recommendations_response = gemini.generate_and_extract(prompt_for_recommended_artists)
                recommendations = recommendations_response["candidates"][0]["content"]["parts"][0]["text"]
                recommendations_as_json = recommendations.strip('```json```').strip()
                parsed_data = json.loads(recommendations_as_json)

                body = format_email_content(filtered_intro, top5_tracks, artists_attributed_to_top_tracks, top5_streams,
                                            top5_album_arts,
                                            top5_artists, top5_listening_minutes_per_artist, top_genres,
                                            recommendations=parsed_data)

                sender_email = os.getenv("MY_EMAIL")
                receiver_email = os.getenv("MY_EMAIL")
                password = os.getenv("APP_PASSWORD")  # Use an app-specific password for better security

                gemini.send_email(subject, body, sender_email, receiver_email, password)
                print("Email sent successfully!")
                last_sent_date = today
                track_songs.melodys_playlist(playlist_name="Melody's Mix")
            else:
                print("Today is not Wednesday. Email not sent.")
            last_time_listened = sheets_data.get_recently_listened_to_time()
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

            if last_time_listened != track_details["time_listened"]:
                logging.info("New track detected, updating spreadsheet.")

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
                    logging.info(f"Last row: {values[-1]}")
                    sheets_data.append_values(sheets)
            else:
                print("No new track, update not needed.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        time.sleep(120)


if __name__ == "__main__":
    main()
