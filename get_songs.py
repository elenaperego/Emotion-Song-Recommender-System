import random

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


def get_playlist_URI(sp, query):
    results = sp.search(q=query, type='playlist', limit=10)
    playlist_uri = results['playlists']['items'][0]['uri']
    return playlist_uri


# maximum of songs is 100
def get_songs(sp, number_of_songs, playlist_uri):
    playlist = sp.playlist(playlist_uri)
    songs = playlist['tracks']['items'][:number_of_songs]
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


"""
input: df of songs matching users emotion
output: next song recommendation (including all features), based on tempo of current song and all next 
"""
def filter_closest_tempo(df_songs, cur_song):
    # no song is playing yet
    if cur_song is None:
        best_rec = df_songs
    # choose next song
    else:
        pl_df_songs = df_songs.copy()  # deep copy of df
        # calculate MAE of possible next song and current one
        pl_df_songs['absolut_tempo_error'] = abs(pl_df_songs['tempo'] - cur_song.loc['tempo'])
        pl_df_songs.sort_values(by=['absolut_tempo_error'], inplace=True)

        # get top 10% of songs
        ind = int(len(pl_df_songs) * 0.1)
        best_rec = pl_df_songs[:ind]

    # randomly select one of the top songs
    ind = random.randint(0, len(best_rec))
    next_song = best_rec.iloc[ind]

    return next_song


# test
#sp = authenticate(client_id, client_secret)
#songs = get_songs(sp, 100, get_playlist_URI(sp, 'very sad'))
#data = create_table_songs(sp, songs)
#data.to_csv('test.csv')
