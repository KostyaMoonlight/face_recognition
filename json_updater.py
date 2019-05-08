import click
import face_recognition
import cv2
import glob
import os
import json 
from utils import *
from db_manager import DBManager
from recognizer import Recognizer



@main.command()
@click.option("--source_folder", "-s", help="Path to folder whick contains labels.")
@click.option("--collection", "-s", help="Collection to save.")
def process_folder(source_folder, collection):
    db = DBManager(collection)
    recognizer = Recognizer(DBManager)
    source_folder = os.path.normpath(source_folder)
    assert os.path.isdir(source_folder), 'Folder does not exist'
    json_files = glob.glob(os.path.join(source_folder, '*.json'))

    for json_file in json_files:
        json_data = load_json(json_file)
        locations, img = get_locations(json_data)
        ids = []
        for location in locations:
            _id = recognizer.recognaze_face(img, location)
            ids.append(_id)
        
        #face_encodings = get_face_encodings(json_data)
        new_json_data = update_ids(json_data, ids)
        save_json(json_file, new_json_data)