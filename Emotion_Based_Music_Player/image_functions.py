import streamlit as st
import numpy as np
from keras.preprocessing.image import img_to_array
from deepface import DeepFace as dfc
from PIL import Image
import cv2


# function to load image
try:
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
except Exception:
    st.write("Error loading cascade classifiers")

@st.cache
def face_detect(img):
    img = np.array(img.convert("RGB"))
    face = face_cascade.detectMultiScale(image=img)

    # draw rectangle around face
    for (x, y, w, h) in face:
        cv2.rectangle(img=img, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
        roi = img[y:y + h, x:x + w]
    return img, face

# analyse image
def analyse_image(img):
    prediction = dfc.analyze(img_path=img)
    return prediction

#function for webcam
def detect_web(image):

    faces = face_cascade.detectMultiScale(
        image=image, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img=image, pt1=(x, y), pt2=(
            x + w, y + h), color=(255, 0, 0), thickness=2)

    return image, faces
