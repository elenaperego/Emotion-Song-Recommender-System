import os
import cv2
import dlib
import numpy as np

# Initialize dlib's face detector, shape predictor, and face recognition model
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')  # Ensure this file is in your project directory
face_rec_model = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')  # Ensure this file is in your project directory

# Lists to store known face encodings and corresponding labels
known_face_encodings = []
known_face_labels = []

# Preferences dictionary
PREFERENCES = {
    'Mischa': ['rock', 'pop', 'classical'],
    'Elena': ['party', 'classical', 'punk'],
    'Meli': ['techno', 'latin', 'jazz'],
    'Lena': ['alternative', 'rap', 'pop']
}

def get_preferences():
    return PREFERENCES

def load_known_faces():
    """
    Load and encode known faces from the database.
    """
    database_folder = 'database'  # Ensure this folder path is correct
    valid_extensions = {".jpg", ".jpeg", ".png"}

    for filename in os.listdir(database_folder):
        ext = os.path.splitext(filename)[1].lower()
        if ext not in valid_extensions:
            continue

        img_path = os.path.join(database_folder, filename)
        label = os.path.splitext(filename)[0]  # Assumes filename is the user's name

        image = cv2.imread(img_path)
        if image is None:
            print(f"Warning: Unable to load image {img_path}. Skipping.")
            continue

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = detector(gray_image)

        if len(faces) == 0:
            print(f"Warning: No face detected in {img_path}. Skipping.")
            continue

        face = faces[0]  # Use the first detected face
        shape = predictor(gray_image, face)
        face_encoding = np.array(face_rec_model.compute_face_descriptor(image, shape))

        known_face_encodings.append(face_encoding)
        known_face_labels.append(label)

def recognize_face(input_image):
    """
    Recognize the face from an input image.
    :param input_image: The image array (BGR format) captured from the webcam.
    :return: Recognized user's name or "Unknown".
    """
    gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray_image)

    if len(faces) == 0:
        return "No face detected"

    face = faces[0]
    shape = predictor(gray_image, face)
    input_face_encoding = np.array(face_rec_model.compute_face_descriptor(input_image, shape))

    # Compute distances between the input face encoding and all known encodings
    distances = np.linalg.norm(known_face_encodings - input_face_encoding, axis=1)

    if len(distances) == 0:
        return "Unknown"

    min_distance_idx = np.argmin(distances)
    min_distance = distances[min_distance_idx]

    if min_distance < 0.6:  # Threshold for recognition
        return known_face_labels[min_distance_idx]
    else:
        return "Unknown"

def get_user_name(img):
    """
    Identify the user from the captured image.
    :param img: The image array (BGR format) captured from the webcam.
    :return: User's name or "Unknown".
    """
    return recognize_face(img)

# Load known faces when the module is imported
load_known_faces()
