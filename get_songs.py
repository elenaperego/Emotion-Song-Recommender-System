import random

import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.preprocessing import StandardScaler


# Mischa's client ID
# Mischa's client ID
client_id = '6e1a09c940a943da95144c6f49a0717b'
client_secret = 'ccc2af43075641f9899eaaac5b716b8b'



def authenticate(client_id, client_secret):
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp


# maximum of songs is 100
def get_songs(sp, number_of_songs, query):
    results = sp.search(q=query, type='playlist')
    playlists = results['playlists']['items'][:100]
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
        track = song.get('track')

        # Check if track is not None
        if track is None:
            continue  # Skip this song if the track information is missing

        id = track.get('id')
        if id is None:
            continue  # Skip if there is no track ID

        # Fetch features for the song; handle case where features may be None or empty
        features_list = sp.audio_features(id)
        features = features_list[0] if features_list and features_list[0] else {}

        # Extract features, handle None values with default fallbacks
        name = track.get('name', 'Unknown')
        album = track['album'].get('name', 'Unknown')
        artist = track['album']['artists'][0].get('name', 'Unknown')
        release_date = track['album'].get('release_date', 'Unknown')
        length = track.get('duration_ms', 0)
        popularity = track.get('popularity', 0)
        acousticness = features.get('acousticness', 0.0)
        danceability = features.get('danceability', 0.0)
        energy = features.get('energy', 0.0)
        instrumentalness = features.get('instrumentalness', 0.0)
        liveness = features.get('liveness', 0.0)
        valence = features.get('valence', 0.0)
        loudness = features.get('loudness', 0.0)
        speechiness = features.get('speechiness', 0.0)
        tempo = features.get('tempo', 0.0)
        key = features.get('key', 0)
        time_signature = features.get('time_signature', 4)  # Default 4/4 time signature

        tracks.append([id, name, album, artist, release_date, popularity, length, danceability, acousticness,
                       energy, instrumentalness, liveness, valence, loudness, speechiness, tempo, key, time_signature])

    columns = ['id', 'name', 'album', 'artist', 'release_date', 'popularity', 'length', 'danceability', 'acousticness',
               'energy', 'instrumentalness', 'liveness', 'valence', 'loudness', 'speechiness', 'tempo', 'key', 'time_signature']
    return pd.DataFrame(tracks, columns=columns)





"""
input: df of songs matching users emotion and preference
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
        ind = (int(len(pl_df_songs) * 0.1)) -1
        best_rec = pl_df_songs[:ind]

    # randomly select one of the top songs
    ind = random.randint(0, len(best_rec)-1)
    next_song = best_rec.iloc[ind]

    return next_song


def filter_emotion(data, emotion):
    scaler = StandardScaler()
    scaler.fit(data[['speechiness', 'loudness']])
    data[['speechiness', 'loudness']] = scaler.transform(data[['speechiness', 'loudness']])
    if emotion == 'Sad':
        data = data[data['speechiness'] > 0.5]
    elif emotion == 'Calm':
        data = data[data['speechiness'] < 0.5]
    elif emotion == 'Happy':
        data = data[data['loudness'] < 0.5]
    else:
        data = data[data['loudness'] > 0.5]
    return data


def get_recommended_song_list(user_name, user_recognition, songs, sp):
    for p in user_recognition.get_preferences().get(user_name):
        songs.extend(get_songs(sp, 50, p))

    return create_table_songs(sp, songs)


# test
sp = authenticate(client_id, client_secret)
songs = get_songs(sp, 300, 'when+you+are+disgusted')
data = create_table_songs(sp, songs)
data.to_csv('when-disgusted.csv')
