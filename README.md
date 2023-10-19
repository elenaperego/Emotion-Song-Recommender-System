# Emotion Music Recommender Interface
## Course Assignment
This repository is part of an assignment for the Intelligent System (KEN-3430) course at Maastricht University.

## Overview
The Emotion Music Recommender Interface is a system that recommends songs based on the user's emotions. It leverages the power of the `spotipy` library to access and play songs on Spotify and the `deepface` library to recognize the user and extract their emotions. As classification model two approaches were tested, a Random forest as well as a Neural Network (NN), with additional song extracting the NN outperformed the Random Forest and therefore was used for classifying songs into mood categories. Songs are being classified into Sad, Calm, Energetic, and Happy the users emotion is mapped onto the same spectrum. To display the application Streamlit is used. Overall, the project aims to bridge the gap between emotions and music, providing users with song recommendations that align with their current mood and music preferences.

## Group Members
- Rosamelia Carioni
- Lena Feiler
- Elena Perego
- Mischa Rauch

## Features
- **Emotion Detection**: Uses the `deepface` library to recognize the user and extract their emotions.
- **Music Recommendation**: Based on the detected emotions, the system recommends songs that match the user's mood.
- **Classification Models**: Two approaches were tested for song classification - a Random Forest and a Neural Network (NN). The NN outperformed the Random Forest and was chosen for classifying songs into mood categories.
- **Mood Categories**: Songs are classified into four moods - Sad, Calm, Energetic, and Happy. The user's emotion is mapped onto the same spectrum.
- **Interactive Interface**: The application uses `Streamlit` for a user-friendly interface.

## [Demonstration Video](https://www.youtube.com/watch?v=n8tmZxU01iw&ab_channel=MischaRauch)
Click on the link above to view a demonstration of the final product.

## How to Run
1. If using conda, first install pip: `conda install pip`
2. Download deepface: `pip install deepface`
3. To run the application, use: `streamlit run main.py` (Ensure you have a picture of yourself in the database so the system can greet you.)

## Resources
- [Music Mood Classification - Tufts University](https://sites.tufts.edu/eeseniordesignhandbook/2015/music-mood-classification/)
- [Predicting the Music Mood of a Song with Deep Learning](https://towardsdatascience.com/predicting-the-music-mood-of-a-song-with-deep-learning-c3ac2b45229e)
- [Music Mood Classification Using Neural Networks and Spotify's Web API](https://medium.com/codex/music-mood-classification-using-neural-networks-and-spotifys-web-api-d73b391044a4)
- [Audio Music Mood Classification](https://neokt.github.io/projects/audio-music-mood-classification/)
- [Music Mood Classification - GitHub](https://github.com/kvsingh/music-mood-classification)
- [Spotify Machine Learning - GitHub](https://github.com/cristobalvch/Spotify-Machine-Learning)

