import os
import json
import cv2
from PIL import Image
import numpy as np

def update_ids(json_data, ids):
        for idx, _id in enumerate(ids):
                json_data['results'][idx]['faceId'] = _id
        return json_data

def get_locations(json_data):
    locations = []
    img_data = get_faces(json_data)
    img_path = get_image_path(json_data)
    img = load_image(img_path)

    for face_attributes in img_data:
        #as an input face_encodings got list of face locations
        face_location = [get_face_rectangle(face_attributes, order='css')]
        locations.extend(face_location)
    return locations, img

def get_face_rectangle(face_attributes, order=''):
    #type: dict -> (int, int, int, int)
    face_rectangle = face_attributes['faceRectangle']
    top, left, width, height = face_rectangle.values()

    if order == 'css':
        # css (top, right, bottom, left) order
        return top, left+width, top+height, left
    return top, left, width, height

def load_image(path):
    #type: str -> numpy
    #cv2.imread couldn't find path
    pil_img = Image.open(path).convert('RGB') 
    img = np.array(pil_img)
    assert img is not None, 'Img is None'
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def get_faces(json_data):
    #type: dict -> list
    return json_data['results']

def get_image_path(json_data):
    #type: dict -> str
    img_path= json_data['imgPath']
    abs_path = os.path.abspath(img_path)
    norm_path = os.path.normpath(abs_path)
    return norm_path

def load_json(path):
    #type: str -> dict

    assert os.path.exists(path), 'Label file does not exist'

    json_data = None
    with open(path, "r") as f:
        json_data = json.load(f)
    return json_data

def save_json(path, json_data):
    #type: str -> None

    assert os.path.exists(path), 'Label file does not exist'
    
    with open(path, "w") as f:
        json.dump(json_data, f)
