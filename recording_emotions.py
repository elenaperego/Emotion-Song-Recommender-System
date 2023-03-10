from deepface import DeepFace
import cv2
import time

current_dominant_emotion = []
current_emotion = []
#mischasPreference = [rock,ambient,]

while True:
    cam = cv2.VideoCapture(0)
    # wait to get enough light for image
    time.sleep(3)
    _, image = cam.read()
    cam.release()
    #cv2.imwrite('test.png',image)
    data = DeepFace.analyze(image)
    #print(data[0].keys())
    # --> dict_keys(['emotion', 'dominant_emotion', 'region', 'age', 'gender', 'dominant_gender', 'race', 'dominant_race'])
    print(data[0].get('dominant_emotion'))
    current_dominant_emotion.append(data[0].get('dominant_emotion'))
    current_emotion.append(data[0].get('emotion'))
    
