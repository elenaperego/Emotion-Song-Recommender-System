# emotion-song-recommender
Recommendation of songs based on facial expression for the Intelligent System course (KEN-3430) at Maastricht University

How to run - for conda use: 
- first install pip (conda install pip)
- download deepface (pip install deepface)


Spotify API https://pypi.org/project/spotify/#Examples inspration: 

TODO: 
1) identify person: input= image, output = name (LOU)
2) filter on preference: input = prefereces, output = list of songs matching preferences (LOU)
3) play random song from list of songs matching preferences: input = list of songs matching preferences, output = playing song (MELI)
4) average emotion: input = list of emotions, output = emotion (LOU)
5) filter on average emotion: input = list of songs matching preferences + average emotion, output = list of songs matching preferences and emotion (INCLUDES: model to classify songs based on emotion https://medium.com/codex/music-mood-classification-using-neural-networks-and-spotifys-web-api-d73b391044a4)) (ELE and MISCHA)
6) filter on tempo: input = list of songs matching preferences and emotion + current song, output = song matching preferences, emotion, and tempo (LOU)
7) play next song (same as 3): input = song matching preferences, emotion, and tempo, output = playing song (MELI)
