import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Mischa's client ID
client_id = '7b663f1643884fd49c296fc676166325'
client_secret = '3e59e5cc8962431ab6127d10e5731f96'


def authenticate(client_id, client_secret):
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp


# maximum of songs is 100
def get_songs(sp, number_of_songs, query):
    results = sp.search(q='genre ' + query, type='playlist')
    playlists = results['playlists']['items'][:10]
    songs = []
    for p in playlists:
        if len(songs) == number_of_songs:
            return songs
        else:
            playlist = sp.playlist(p['uri'])
            temp = playlist['tracks']['items'][:(number_of_songs - len(songs))]
            songs.extend(temp)
    return songs


def create_table_songs(sp, songs):
    tracks = []
    for song in songs:
        track = song['track']
        id = track['id']
        features = sp.audio_features(id)
        name = track['name']
        album = track['album']['name']
        artist = track['album']['artists'][0]['name']
        release_date = track['album']['release_date']
        length = track['duration_ms']
        popularity = track['popularity']
        acousticness = features[0]['acousticness']
        danceability = features[0]['danceability']
        energy = features[0]['energy']
        instrumentalness = features[0]['instrumentalness']
        liveness = features[0]['liveness']
        valence = features[0]['valence']
        loudness = features[0]['loudness']
        speechiness = features[0]['speechiness']
        tempo = features[0]['tempo']
        key = features[0]['key']
        time_signature = features[0]['time_signature']
        tracks.append([id, name, album, artist, release_date, popularity, length, danceability, acousticness,
                       energy, instrumentalness, liveness, valence, loudness, speechiness, tempo, key, time_signature])
    columns = ['id', 'name', 'album', 'artist', 'release_date', 'popularity', 'length', 'danceability', 'acousticness',
               'energy', 'instrumentalness',
               'liveness', 'valence', 'loudness', 'speechiness', 'tempo', 'key', 'time_signature']

    return pd.DataFrame(tracks, columns=columns)


# test
sp = authenticate(client_id, client_secret)
songs = get_songs(sp, 200, 'rock')
data = create_table_songs(sp, songs)
print(data['speechiness'].describe())
# data.to_csv('very_sadSongs.csv')
