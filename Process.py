import os
from keras.preprocessing.image import img_to_array
from flask import jsonify
from keras.backend import clear_session
import imutils
import cv2
from keras.models import load_model
import numpy as np
import datetime


UPLOAD_FOLDER = 'media'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
detection_model_path = 'haarcascade_files/haarcascade_frontalface_default.xml'
emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'


def process(img):
    clear_session()

    face_detection = cv2.CascadeClassifier(detection_model_path)
    emotion_classifier = load_model(emotion_model_path, compile=False)
    frame = cv2.imread(os.path.join(img), cv2.IMREAD_GRAYSCALE)
    frame = imutils.resize(frame, width=300)
    faces = face_detection.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                            flags=cv2.CASCADE_SCALE_IMAGE)
    print("detecting faces")
    # print(img)
    # cv2.imshow("1",frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    em = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]
    if len(faces) > 0:

        for ele in faces:
            (x, y, w, h) = ele
            roi = frame[y:y + h, x:x + w]
            roi = cv2.resize(roi, (64, 64))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            preds = emotion_classifier.predict(roi)[0]

        with open("data.txt") as f:
            dictionary = {}
            for line in f:
                dictionary[line.split(':')[0]] = int(line.split(':')[1].rstrip('\n'))
        ele = str(em[list(preds).index(max(list(preds)))])
        emotion = {
            "angry": str(preds[0]),
            "disgust": str(preds[1]),
            "scared": str(preds[2]),
            "happy": str(preds[3]),
            "sad": str(preds[4]),
            "surprised": str(preds[5]),
            "neutral": str(preds[6]),
            "data": ele,
            "num": dictionary[ele]
        }
    else:
        print("Face not found")

        emotion = {
            "data": "no face detected",
        }
    logfile = str(datetime.datetime.now()).split(" ")[0] + ".txt"
    with open(os.path.join(os.path.join(UPLOAD_FOLDER, str(img).split('\\')[1]), logfile), "a") as f:
        f.writelines("{} - {}\n".format(str(emotion), str(datetime.datetime.now()).split(" ")[1]))

    return jsonify(emotion)
