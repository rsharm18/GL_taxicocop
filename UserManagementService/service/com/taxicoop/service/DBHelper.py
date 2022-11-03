import pprint
from datetime import datetime, timedelta
# from bson.objectid import ObjectId

import pymongo

db_conn = pymongo.MongoClient(
    "mongodb+srv://taxicoop:admin123@cluster0.ykco3.mongodb.net/?retryWrites=true&w=majority")

db = db_conn["user_management"]


class Database:

    # This method finds a single document using field information provided in the key parameter
    # It assumes that the key returns a unique document. It returns None if no document is found
    @staticmethod
    def get_single_data(key):
        document = db.find_one(key)
        return document

    # This method inserts the data in a new document. It assumes that any uniqueness check is done by the caller
    @staticmethod
    def insert_single_data(data):
        document = db.insert_one(data)
        return document.inserted_id

    @staticmethod
    def get_all_user():
        return db.find()

