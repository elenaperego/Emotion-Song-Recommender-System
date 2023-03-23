import os
import numpy as np
from deepface import DeepFace
import cv2
import get_songs as gs
import time
import models.load_model as model_library
import user_recognition
#from play_song import play_current_song
import webbrowser
import streamlit as st
import get_url_song


# Ele's client ID
CLIENT_ID = '6e1a09c940a943da95144c6f49a0717b'
CLIENT_PASSWORD = 'ccc2af43075641f9899eaaac5b716b8b'
sp = gs.authenticate(CLIENT_ID, CLIENT_PASSWORD)
allowed_margin_to_change_song = 60 # amount in seconds

binary_to_emotion = { 0 : 'Sad', 1 : 'Calm', 2 :  'Energetic', 3 : 'Happy' }
emotion_to_binary = { 'angry' : 2, 'disgust' : 0, 'fear' : 1, 'happy' : 3, 'sad' : 0, 'surprise' : 2, 'neutral' : 1}
dominant_emotions = []
# current playing song
current_song = None
# list of all songs matching the users preferences
songs = []


def highest_occurrence(strings):
    occurrences = {}
    for string in strings:
        if string in occurrences:
            occurrences[string] += 1
        else:
            occurrences[string] = 1
    return max(occurrences, key=occurrences.get)

# Define a function to update the content of column 2
def update_col_content(column,new_content):
    column.markdown(new_content)


if __name__ == "__main__":
    st.title("Emotion Song Recommender!")
    st.subheader('The first recommedation is based on your preferences and not on your current emotion')
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("This is your pretty face ;)")
        picture = st.camera_input("")

    cam = cv2.VideoCapture(0)
    time.sleep(3)
    _, image = cam.read()
    cam.release()

    # user identification
    cam_path = "/database/current_user.png"
    user_name = user_recognition.get_user_name(image, cam_path)
    st.header("Welcome back "+user_name)

    # Get random song
    data = gs.get_recommended_song_list(user_name, user_recognition, songs, sp)

    current_song = gs.filter_closest_tempo(data, current_song)
    
    recommendation = get_url_song.get_current_song(current_song['artist'],current_song['name'],sp)

    update_col_content(col3,"To listen to your song recommendation, please click the folllowing link.")
    update_col_content(col3,recommendation)
    update_col_content(col2,"We detect that you are currently feeling: ")

    start_time = time.time() # seconds
    length_song = current_song.loc['length'] / 1000 
    
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
        dominant_emotions.append(binary_emotion)
        print("BINARY ",binary_emotion)

        # TODO: 30 back to lengt_song
        if (elapsed_time > length_song - allowed_margin_to_change_song):

            # get average of current_dominant_emotion (string) and clear the old list
            current_emotion = highest_occurrence(dominant_emotions)
            dominant_emotions.clear()

            print("EMOTION ",current_emotion)
    
            # get songs based on preference
            data = gs.get_recommended_song_list(user_name, user_recognition, songs, sp)

            # Classify on emotion with model (NN or RF) taking into account the current dominant emotion
            # returns a df of songs matching the two possible emotion
            filtered_data = model_library.predict_emotions_nn(data,binary_emotion)


            # Filter/Order on sad or calm = speechiness --> high speechiness = sad, energetic and happy = loudness --> high loudness = energetic
            # returns data in a df of songs matching emotion with a filter of < 0.5 based on the emotion
            data = gs.filter_emotion(data, current_emotion)

            # returns next song recommendation 
            current_song = gs.filter_closest_tempo(data, current_song)
            cur_song_name = current_song.loc['name']  # TODO put into streamline
            print(cur_song_name)


            # After new song starts playing, we update all time variables
            length_song = current_song.loc['length']/1000
            start_time = time.time()

            recommendation = get_url_song.get_current_song(current_song['artist'],current_song['name'],sp)

            update_col_content(col2, '')
            update_col_content(col2, binary_to_emotion.get(current_emotion))
            update_col_content(col3, '')
            update_col_content(col3,recommendation)

