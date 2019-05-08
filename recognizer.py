import face_recognition
import cv2


class Recognizer():

    def __init__(self, db_manager, transform = None):
        '''
        Args:
            db_manager(DBManager): database manager which handles information with people and their encodings
            transform(func): transforms applied to the image before recognition
        '''
        super(Recognizer, self).__init__()
        self.db_manager = db_manager
        self.transform = self._transform
        if transform:
            self.transform = transform

    def _transform(self, img):
        return img

    def recognaze_face(self, face, face_location):
        face_encoding = face_recognition.face_encodings(face, face_location)
        encodings = [enc['encoding'] for enc in self.db_manager.get_encodings()]          
        ids = [enc['_id'] for enc in self.db_manager.get_ids()]
        matches = face_recognition.compare_faces(encodings, face_encoding)

        if True in matches:
            first_match_index = matches.index(True)
            _id = ids[first_match_index]
        else:
            _id = self.db_manager.add_user({'encoding':face_encoding.tolist()})
        return _id, face_encoding   

    def recognize(self, frame):
        '''
        Recognize people on the frame comparing them with database
        Args:
            frame(nparray): current frame
        '''
        if frame is None:
            raise Exception('You did not pass any image')
            
        
        frame = self.transform(frame)
        face_ids = []
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        clients = []
        for face_encoding in face_encodings:
            encodings = [enc['encoding'] for enc in self.db_manager.get_encodings()]
            
            ids = [enc['_id'] for enc in self.db_manager.get_ids()]

            matches = face_recognition.compare_faces(encodings, face_encoding)

            if True in matches:
                first_match_index = matches.index(True)
                _id = ids[first_match_index]
            else:
                _id = self.db_manager.add_user({'encoding':face_encoding.tolist()})
        clients.append(_id)   
        return clients


