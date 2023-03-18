import os
import numpy as np
from deepface import DeepFace
import cv2
import get_songs as gs
import time
import models.load_model as model_library
import user_recognition

from sklearn.preprocessing import StandardScaler

# Ele's client ID
CLIENT_ID = '6e1a09c940a943da95144c6f49a0717b'
CLIENT_PASSWORD = 'ccc2af43075641f9899eaaac5b716b8b'
sp = gs.authenticate(CLIENT_ID, CLIENT_PASSWORD)

def highest_occurrence(strings):
    occurrences = {}
    for string in strings:
        if string in occurrences:
            occurrences[string] += 1
        else:
            occurrences[string] = 1
    return max(occurrences, key=occurrences.get)

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

# TODO: MOVE ALL THE STUFF THAT IS NOT GLOBAL VARIABLES TO MAIN METHOD
moods= {'Sad' : 0, 'Calm' : 1, 'Energetic' : 2, 'Happy' : 3}

allowed_margin_to_change_song = 20 # amount in seconds

# --> Sad' : 0, 'Calm' : 1, 'Energetic' : 2, 'Happy' : 3
emotion_to_binary = { 'angry' : 0, 'disgust' : 2, 'fear' : 1, 'happy' : 3, 'sad' : 0, 'surprise' : 2, 'neutral' : 1}
current_dominant_emotion = []
current_emotion = []
current_song = None

preferences = {'Mischa': ['rock', 'pop', 'classical'],
               'Elena': ['party', 'classical', 'punk'],
               'Meli': ['techno', 'latin', 'jazz'],
               'Lena': ['alternative', 'rap', 'pop']}


cam = cv2.VideoCapture(0)
time.sleep(3)
_, image = cam.read()
cam.release()

# TODO (LOU): Identify person 
# user identification
cam_path = "/database/current_user.png"
user_name = user_recognition.get_user_name(image, cam_path)

# TODO: Get random song from preference list of user

# Get random song
songs = gs.get_songs(sp, 100, gs.get_playlist_URI(sp, preferences.get(user_name)[0]))
songs.extend(gs.get_songs(sp, 100, gs.get_playlist_URI(sp, preferences.get(user_name)[1])))
songs.extend(gs.get_songs(sp, 100, gs.get_playlist_URI(sp, preferences.get(user_name)[2])))
data = gs.create_table_songs(sp, songs)

current_song = data.sample(1) # Assuming is a df with one sample


if __name__ == "__main__":

    start_time = time.time() # seconds
    # TODO: before getting the length store random song from preference in df
    length_song = current_song['length'].values[0] / 1000 
    while True:
        elapsed_time = time.time() - start_time
        cam = cv2.VideoCapture(0)
        # wait to get enough light for image
        time.sleep(3)
        _, image = cam.read()
        cam.release()
        data = DeepFace.analyze(image, enforce_detection=False)
        # --> dict_keys(['emotion', 'dominant_emotion', 'region', 'age', 'gender', 'dominant_gender', 'race', 'dominant_race'])
        binary_emotion = emotion_to_binary.get(data[0].get('dominant_emotion'))
        current_dominant_emotion.append(binary_emotion)
        print("BINARY ",binary_emotion)
        # TODO (MISCHA): refactor the current emotion to our available list --> Sad' : 0, 'Calm' : 1, 'Energetic' : 2, 'Happy' : 3
        #current_dominant_emotion.append(data[0].get('dominant_emotion'))
        #current_emotion.append(data[0].get('emotion'))

        if (elapsed_time > length_song - allowed_margin_to_change_song):

            # TODO (MELI): get average of current_dominant_emotion and clear the old list
            emotion = highest_occurrence(current_dominant_emotion)
            current_dominant_emotion.clear()

            # get songs based on preference
            songs = gs.get_songs(sp, 100, gs.get_playlist_URI(sp, preferences.get(user_name)[0]))
            songs.extend(gs.get_songs(sp, 100, gs.get_playlist_URI(sp, preferences.get(user_name)[1])))
            songs.extend(gs.get_songs(sp, 100, gs.get_playlist_URI(sp, preferences.get(user_name)[2])))
            data = gs.create_table_songs(sp, songs)
            print("EMOTION ",emotion)
    

            songs = []
            # get songs based on preference
            for p in preferences.get(user_name):
                songs.extend(gs.get_songs(sp, 100, gs.get_playlist_URI(sp, p)))

            data = gs.create_table_songs(sp, songs)

            # TODO (MISCHA): Classify on emotion with model (NN or RF) taking into account the current dominant emotion
            # TODO (MISCHA): Play around with NN 
            # returns a df of songs matching the two possible emotion
            filtered_data = model_library.predict_emotions_rf(data,binary_emotion)


            # TODO (ELENA): Filter/Order on sad or calm = speechiness --> high speechiness = sad, energetic and happy = loudness --> high loudness = energetic
            # IF time: filter songs based on realeased date matching with the age of the user
            # returns data in a df of songs matching emotion with a filter of < 0.5 based on the emotion
            data = filter_emotion(data, current_emotion)

            # TODO (LOOU): Tempo: create a new column (absolut_tempo_error) where the previous tempo .... you will figure it out
            # returns one song
            song_rec = gs.filter_closest_tempo(data, current_song)
            current_song = song_rec
            cur_song_name = song_rec.loc['name']
            print(cur_song_name)


            # After new song starts playing, we update all time variables
            # TODO: update the database  --> current_song =
            length_song = current_song['length'][0]/1000
            start_time = time.time()



    # TODO (MELI / ALL): Play song
