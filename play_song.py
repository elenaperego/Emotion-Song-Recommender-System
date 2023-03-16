import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser

def play_song(artist, track, authentication):
    # search in spotify
    results = authentication.search(q=f"artist:{artist} track:{track}")

    # extract URL from results
    entire_song = results["tracks"]["items"][0]["external_urls"]["spotify"]
    thirty_seconds = results["tracks"]["items"][0]["preview_url"]

    # open browser
    webbrowser.open(thirty_seconds)
    #print(entire_song)

# TODO: not sure what structure the list of songs will have ?
def play_random_song(songs, authentication):
    return 0

# Testing

# Ele's client ID
SPOTIPY_CLIENT_ID = "6e1a09c940a943da95144c6f49a0717b"
SPOTIPY_CLIENT_SECRET = "ccc2af43075641f9899eaaac5b716b8b"

authentication = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET
    )
)


artist = "Elijah Waters"
track = "Someone Special"
play_song(artist, track, authentication)


