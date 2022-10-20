import pymongo

from ride_management_service.service.com.taxicoop.model.Ride_Request import Ride_Request

db_client = pymongo.MongoClient(
    "mongodb+srv://taxicoop:admin123@cluster0.ykco3.mongodb.net/?retryWrites=true&w=majority")

db = db_client.test
# Create a Database
ride_mgmt_db = db_client['ride_management']
# Create Collections
ride_request = ride_mgmt_db['ride_request']
trip_summary = ride_mgmt_db['trip_summary']


class DB_Helper:

    @staticmethod
    def register_new_ride_request(ride: Ride_Request):
        print(ride.__dict__)
        ride_request.insert_one(ride.__dict__)
