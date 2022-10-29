import pprint
from datetime import datetime, timedelta

import pymongo
import certifi
from bson import SON
from com.taxicoop.dto.NearByTaxiDTO import NearByTaxis
from com.taxicoop.model.Location import Location
from com.taxicoop.model.Taxi import Taxi
from com.taxicoop.setup.Data_Generator import Data_Generator
from haversine import haversine, Unit

from com.taxicoop.model.Taxi import Taxi_Type, Taxi_Status

DEFINED_RADIUS = 5000


db_client = pymongo.MongoClient(
    "mongodb+srv://taxicoop:admin123@cluster0.ykco3.mongodb.net/?retryWrites=true&w=majority",
     tlsCAFile=certifi.where()
)

db = db_client.test
# Create a Database
user_mgmt_db = db_client['user_management']
# Create Collections
users = user_mgmt_db['users']


class DB_Helper:

    # db = client.test

    @staticmethod
    def configure_db():
        count = users.estimated_document_count()
        if count == 0:
            print("Adding dummy Data")
            data = Data_Generator.generate_taxi_data(50)
            users.insert_many(data)

    @staticmethod
    def register_User(user: User):
        users.insert_one(user.__dict__)


    @staticmethod
    def get_all_Users():
        return user.find()


    @staticmethod
    def get_user_by_user_ids(user_ids=None):
        if user_ids is None:
            return []

        print("user_ids {}".format(user_ids))
        users.find({'user_id': {'$in': user_ids}})
        return users


    @staticmethod
    def delete_stale_data():
        from_range = datetime.today() - timedelta(minutes=max_minutes_stale_data)

        print("from_range {}".format(from_range))

        criteria = {"timestamp": {"$lte": from_range}}
        users.delete_many(criteria)

    @staticmethod
    def update_User(user_id, values):
        query = {"user_id": user_id}
        update = {"$set": values}
        user_data = users.find_one(query)
        if user_data is None:
            raise Exception("Invalid Taxi id")

        users.update_one(query, update)
