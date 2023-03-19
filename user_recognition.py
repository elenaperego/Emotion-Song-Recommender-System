import os.path
import cv2
from deepface import DeepFace



PREFERNCES = {'Mischa': ['rock', 'pop', 'classical'],
               'Elena': ['party', 'classical', 'punk'],
               'Meli': ['techno', 'latin', 'jazz'],
               'Lena': ['alternative', 'rap', 'pop']}


def get_preferences():
    return PREFERNCES

"""
output: list of paths to all images in the database (of users)
"""
def get_all_image_paths():
    folder_name = '/database'
    imgs = []
    path = os.getcwd() + folder_name
    valid_images = [".jpg"]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        imgs.append(os.getcwd() + folder_name + "/" + f)

    return imgs


def save_img(img, img_name):
    cv2.imwrite(os.getcwd() + img_name, img)


def identify_user(cam_path, img_paths):
    for img in img_paths:
        result = DeepFace.verify(img1_path=cam_path, img2_path=img)
        if result.get('verified'):
            ph = (img.split("/")[-1])
            user = ph.split(".")[0]
            return user


def get_user_name(img, cam_path):
    img_paths = get_all_image_paths()
    save_img(img, cam_path)  # save current webcam image
    return identify_user(os.getcwd() + cam_path, img_paths)
