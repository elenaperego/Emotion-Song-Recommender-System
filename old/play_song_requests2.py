import requests


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

# Set up the necessary headers and data for the request
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token),
    'Content-Type': 'application/json'
}
data = {
    "context_uri": "spotify:album:5ht7ItJgpBH7W6vJ5BqpPr",
    "offset": {
        "position": 5
    },
    "position_ms": 0
    #'device_id': '0d1841b0976bae2a3a310dd74c0f3df354899bc8'
}

# Send the request to the Spotify API
url = 'https://api.spotify.com/v1/me/player/play'
response = requests.put(url, headers=headers, json=data)

# Check the status code of the response to confirm whether the request was successful
if response.status_code == 204:
    print('Track is now playing.')
else:
    print('Failed to play track.')
    print(response.json())
