import cv2
import numpy as np
from threading import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("firbase-key\replace firebase json file")
firebase_admin.initialize_app(cred, {
    'databaseURL':'replace firebase url'
})

def capture():
    face_cascade = cv2.CascadeClassifier("xml\haarcascade_frontalface_default.xml")
    videocapture = cv2.VideoCapture(0)
    scale_factor = 1.3

    while 1:
        ret, pic = videocapture.read()
        faces = face_cascade.detectMultiScale(pic, scale_factor, 5)

        for (x, y,w, h) in faces:
            cv2.rectangle(pic, (x, y), (x + w, y+ h), (255, 0, 255), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX

        y = format(len(faces))
        number = str(y)

        x = Thread(target=myfirebase, args=(number,pic))
        x.start()

        cv2.imshow('face', pic)
        k = cv2.waitKey(30) & 0xff
        if k == 2:
            break

    cv2.destroyAllWindows()

def myfirebase(number,pic):
    ref = db.reference('/python')
    ref.set({
        'cammera_count':
            {
            'face_count': number
        }
    })
    #print(number)
    return number

capture()
