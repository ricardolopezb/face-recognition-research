import face_recognition as fr
import cv2 as cv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
import skimage

Tk().withdraw()
load_image = askopenfilename()

target_image=fr.load_image_file(load_image)
target_encoding=fr.face_encodings(target_image)

urls = {
    "TRUMP": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Donald_Trump_official_portrait.jpg/1200px-Donald_Trump_official_portrait.jpg",
    "PUTIN": f"https://upload.wikimedia.org/wikipedia/commons/5/51/%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%BC%D0%B8%D1%80_%D0%9F%D1%83%D1%82%D0%B8%D0%BD_%2818-06-2023%29_%28cropped%29.jpg",
    "BORIS": f"https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Boris_Johnson_official_portrait_%28cropped%29.jpg/800px-Boris_Johnson_official_portrait_%28cropped%29.jpg"
}

# Searches for ocurrences of this face
def encode_faces (folder):
    list_people_encoding = []
    for filename in os.listdir(folder):
        known_image=fr.load_image_file(f'{folder}{filename}')
        print(type(known_image))
        know_encoding=fr.face_encodings(known_image)[0]
        list_people_encoding.append((know_encoding,filename))
    return list_people_encoding

def encode_faces_with_URL_source(urls):
    list_people_encoding = []
    for person_name, url in urls.items():
        image_filename = url
        print("IMAGEFILENAME", image_filename)
        known_image = skimage.io.imread( image_filename )
        know_encoding=fr.face_encodings(known_image)[0]
        list_people_encoding.append((know_encoding, person_name))
    return list_people_encoding


def are_all_boolean_value(x, bool_list):
    for value in bool_list:
        if value != x:
            return False
    return True

def find_target_face():
    face_location = fr. face_locations(target_image)
    #for person in encode_faces('people/'):
    for person in encode_faces_with_URL_source(urls):
        encoded_face = person[0]
        filename = person[1]
        is_target_face = fr.compare_faces(encoded_face, target_encoding, tolerance=0.55)
        print (f'{is_target_face} {filename}')
        if face_location:
            face_number = 0
            for location in face_location:
                if is_target_face[face_number]:
                    label = filename
                    create_frame(location, label)
                elif are_all_boolean_value(False, is_target_face):
                    label = "Unknown"
                    create_frame(location, label)
                face_number +=1 
                #create_frame(location, label)
                #face_number +=1


def create_frame (location, label):
    top, right, bottom, left = location
    cv.rectangle(target_image, (left, top), (right, bottom), (255, 0, 0), 2)
    cv. rectangle(target_image, (left, bottom + 20), (right, bottom), (255, 0, 0), cv.FILLED)
    cv. putText (target_image, label, (left + 3, bottom + 14), cv.FONT_HERSHEY_DUPLEX, 0.4, (255,255,255), 1)

def render_image():
    rgb_img=cv.cvtColor(target_image, cv.COLOR_BGR2RGB)
    cv.imshow('Face Recognition', rgb_img)
    cv.waitKey(0)

find_target_face()
render_image()