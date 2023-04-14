# emotion-song-recommender
### Group Members: Rosamelia Carioni, Lena Feiler, Elena Perego, Mischa Rauch

#### This repository is part of an assignment for a course in Intelligent System (KEN-3430) at Maastricht University.


This project uses the spotipy library to access and play songs on spotify. The deepface library to recognize the user and extract emotions of the user. As classification model two approaches were tested, a Random forest as well as a Neural Network (NN), with additional song extracting the NN outperformed the Random Forest and therefore was used for classifying songs into mood categories. Songs are being classified into Sad, Calm, Energetic, and Happy the users emotion is mapped onto the same spectrum. To display the application Streamlit is used. 

How to run - for conda use: 
- first install pip (conda install pip)
- download deepface (pip install deepface)

To run the application use 'streamlit run main.py' (make sure you have a picture of yourself in the database such that the system can greet you ;))


RESOURCES: 
Music Classification:
- https://sites.tufts.edu/eeseniordesignhandbook/2015/music-mood-classification/
- https://towardsdatascience.com/predicting-the-music-mood-of-a-song-with-deep-learning-c3ac2b45229e
- https://medium.com/codex/music-mood-classification-using-neural-networks-and-spotifys-web-api-d73b391044a4
- https://neokt.github.io/projects/audio-music-mood-classification/
- https://github.com/kvsingh/music-mood-classification
- https://github.com/cristobalvch/Spotify-Machine-Learning

