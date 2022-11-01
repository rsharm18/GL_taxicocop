import pprint
from datetime import datetime, timedelta
from bson.objectid import ObjectId

import pymongo
import certifi


class Database:
    DB_NAME = 'user_management'

    # collection ='users'

    def __init__(self):
        self.db_conn = pymongo.MongoClient(
            "mongodb+srv://taxicoop:admin123@cluster0.ykco3.mongodb.net/?retryWrites=true&w=majority",
            tlsCAFile=certifi.where()
        )
        self.db = self.db_conn[Database.DB_NAME]

    # This method finds a single document using field information provided in the key parameter
    # It assumes that the key returns a unique document. It returns None if no document is found
    def get_single_data(self, collection, key):
        db_collection = self.db[collection]
        document = db_collection.find_one(key)
        return document

    # This method inserts the data in a new document. It assumes that any uniqueness check is done by the caller
    def insert_single_data(self, collection, data):
        db_collection = self.db[collection]
        document = db_collection.insert_one(data)
        return document.inserted_id


class UserModel:
    USER_COLLECTION = 'users'

    def __init__(self):
        self.db = Database()
        self._latest_error = ''

    @property
    def latest_error(self):
        return self._latest_error

    # Since username should be unique in users collection, this provides a way to
    # fetch the user document based on the Email
    def find_by_username(self, username):
        key = {'username': username}
        return self.__find(key)

    # Finds a document based on the unique auto-generated MongoDB object id
    def find_by_object_id(self, obj_id):
        key = {'_id': ObjectId(obj_id)}
        return self.__find(key)

    # Private function (starting with __) to be used as the base for all find functions
    def __find(self, key):
        user_document = self.db.get_single_data(UserModel.USER_COLLECTION, key)
        return user_document

    # This first checks if a user already exists with that username. If it does, it populates latest_error and returns -1
    # If a user doesn't already exist, it'll insert a new document and return the same to the caller
    def insert_user(self, username, email, contact_info):
        self._latest_error = ''
        user_document = self.find_by_username(email)
        if (user_document):
            self._latest_error = f'Username {email} already exists'
            return -1
        user_data = {'username': username, 'email': email, 'contact_info': contact_info}
        user_obj_id = self.db.insert_single_data(UserModel.USER_COLLECTION, user_data)
        return self.find_by_object_id(user_obj_id)

    def get_all_Users(self):
        Users = UserModel.USER_COLLECTION.find()
        result = []
        for user in Users:
            name = user['username']
            email = user['email']
            contact_info = user['contact_info']
            result.append(name=name, email=email, contact_info= contact_info ).__dict__

        return result

