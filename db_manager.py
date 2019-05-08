import face_recognition
import cv2
import glob
from pymongo import MongoClient
from bson import ObjectId
import os

def get_fullname(image_name):
    '''
    Get name of photo. Remove all numbers from it.
    '''
    base_name = os.path.basename(image_name)
    base_name = os.path.splitext(base_name)[0]
    clear_base_name = ''.join([i for i in base_name if not i.isdigit()]).split('_')
    name, surname = clear_base_name[0], clear_base_name[1]
    return name, surname

class DBManager():
    def __init__(self, collention='clients'):
        super(DBManager, self).__init__()
        self.client = MongoClient('localhost', 27017)
        self.db = self.client["face_id"]
        self.clients = self.db[collention]
        #self.fill_collection()

    def get_collection(self):
        return self.clients.find({})

    def get_user(self, _id):
        return self.clients.find_one({'_id':ObjectId(_id)})

    def get_ids(self):
        return self.clients.find({}, { '_id':1})

    def get_encodings(self):
        return self.clients.find({}, { 'encoding':1, '_id':0})

    def get_clients(self, ids):
        return self.clients.find({ "_id": { "$in": ids }})

    
    def add_user(self, user):
        try: 
            print(user)
            user = self.clients.insert_one(user)
            return user.inserted_id
        except:
            raise Exception('Could not add to database')


if __name__ == "__main__":
    db_manager = DBManager()


    