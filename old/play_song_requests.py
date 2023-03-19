import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

url = 'https://api.spotify.com/v1/me/player/play'

USER_ID = '31bkmllknst2codaz4pqdksjrlha'
TOKEN = 'BQAXY0cnj5vnsZhSu6ttqb6rnGbLUgt9-O9MJ8ebafDqXJtJyVzuHxtJtzomXvwQXlZAABV8u6TDpDRvd8hlgrq5apziKu0RAxnw2_UMW2ReeRmipLlPl60_pL3AXZUKvuL6mc39sI2n8FWKsdvggvAchklisxiyreyHdL36jA3k7Lp8'


#headers = {
        #"Accept" : "application/json",
        #"client_id" : "7b663f1643884fd49c296fc676166325",
        #"client_secret" : "3e59e5cc8962431ab6127d10e5731f96",
#        "device_id" : "0d1841b0976bae2a3a310dd74c0f3df354899bc8",
        #"Content-Type" : "application/json",
#        "Authorization" : "Bearer {token}".format(token=TOKEN)
#    }

myobj = {
    "context_uri": "spotify:album:5ht7ItJgpBH7W6vJ5BqpPr",
    "offset": {
        "position": 5
    },
    "position_ms": 0
}

CLIENT_ID = '7b663f1643884fd49c296fc676166325'
CLIENT_SECRET = '3e59e5cc8962431ab6127d10e5731f96'


########
AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']

print("ACCES TOKEN ",access_token)

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

# Track ID from the URI
track_id = '6y0igZArWVi6Iz0rj35c1Y'

# actual GET request with proper header
r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)

print(" R : ",r.json())
########


def authenticate(client_id, client_secret):
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp


sp = authenticate(CLIENT_ID, CLIENT_SECRET)

x = requests.post(url, headers= headers, json = myobj)

print("X ",x.text)