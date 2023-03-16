import os
from deepface import DeepFace
import cv2
import time
import get_songs
import user_recognition

moods = {'Sad': 0, 'Calm': 1, 'Energetic': 2, 'Happy': 3}

# Ele's client ID
client_id = '6e1a09c940a943da95144c6f49a0717b'
client_secret = 'ccc2af43075641f9899eaaac5b716b8b'

sp = get_songs.authenticate(client_id, client_secret)

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

# user identification
cam_path = "/database/current_user.png"
user_name = user_recognition.get_user_name(image, cam_path)


while True:
    cam = cv2.VideoCapture(0)
    # wait to get enough light for image
    time.sleep(3)
    _, image = cam.read()
    cam.release()
    data = DeepFace.analyze(image)

    # --> dict_keys(['emotion', 'dominant_emotion', 'region', 'age', 'gender', 'dominant_gender', 'race', 'dominant_race'])
    print(data[0].get('dominant_emotion'))
    # TODO (MISCHA): refactor the current emotion to our available list --> Sad' : 0, 'Calm' : 1, 'Energetic' : 2, 'Happy' : 3
    current_dominant_emotion.append(data[0].get('dominant_emotion'))
    current_emotion.append(data[0].get('emotion'))

    # TODO (MELI): Check time if time is ready do calculations below (IF not) otherwise collect emotions (go up to the code 'continue')

    # TODO (MELI): get average of current_dominant_emotion and clear the old list

    songs = []
    # get songs based on preference
    for p in preferences.get(user_name):
        songs.extend(get_songs.get_songs(sp, 100, get_songs.get_playlist_URI(sp, p)))

    data = get_songs.create_table_songs(sp, songs)

    # TODO (MISCHA): Classify on emotion with model (NN or RF) taking into account the current dominant emotion
    # TODO (MISCHA): Play around with NN 
    # returns a df of songs matching the two possible emotion

    # TODO (ELENA): Filter/Order on sad or calm = speechiness --> high speechiness = sad, energetic and happy = loudness --> high loudness = energetic
    # IF time: filter songs based on realeased date matching with the age of the user
    # returns data in a df of songs matching emotion with a filter of < 0.5 based on the emotion

    song_rec = get_songs.filter_closest_tempo(data, current_song)
    current_song = song_rec
    cur_song_name = song_rec.loc['name']
    print(cur_song_name)

    # TODO (MELI / ALL): Play song
