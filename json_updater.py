import click
import face_recognition
import cv2
import glob
import os
import json 
from utils import *
from db_manager import DBManager
from recognizer import Recognizer


@click.group()
def main():
    pass

@main.command()
@click.option("--source_folder", "-s", help="Path to folder whick contains labels.")
@click.option("--collection", "-s", help="Collection to save.")
def process_folder(source_folder, collection):
    db = DBManager(collection)
    recognizer = Recognizer(db)
    source_folder = os.path.normpath(source_folder)
    assert os.path.isdir(source_folder), 'Folder does not exist'
    labels_folder = os.path.join(source_folder, 'labels')
    first_subfolders = [os.path.join(labels_folder, l) for l in os.listdir(labels_folder)]
    for first_subfolder in first_subfolders:
        second_subfolders = [os.path.join(first_subfolder, l) for l in os.listdir(first_subfolder)]
        for second_subfolder in second_subfolders:
            json_files = glob.glob(os.path.join(second_subfolder, '*.json'))
            for json_file in json_files:
                json_data = load_json(json_file)
                locations = get_locations(json_data, second_subfolder)
                if locations is None:
                    continue
                locations, img = locations
                ids = []
                for location in locations:
    
                    _id = recognizer.recognaze_face(img, location)
                    ids.append(_id)
                
                #face_encodings = get_face_encodings(json_data)
                new_json_data = update_ids(json_data, ids)
                save_json(json_file, new_json_data)

if __name__ == "__main__":
    main()