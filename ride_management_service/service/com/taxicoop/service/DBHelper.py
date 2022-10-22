from pymongo import MongoClient, GEOSPHERE

from com.taxicoop.model.Ride_Request import Ride_Request

db_client = MongoClient(
    "mongodb+srv://taxicoop:admin123@cluster0.ykco3.mongodb.net/?retryWrites=true&w=majority")

db = db_client.test
# Create a Database
ride_mgmt_db = db_client['ride_management']
# Create Collections
ride_request = ride_mgmt_db['ride_request']
trip_summary = ride_mgmt_db['trip_summary']

# Create Index(es)
ride_request.create_index([('location', GEOSPHERE)])


class DB_Helper:

    @staticmethod
    def register_new_ride_request(ride: Ride_Request):
        print(ride.__dict__)
        ride_request.insert_one(ride.__dict__)

    @staticmethod
    def update_ride_request(ride_request_id, values):
        query = {"ride_request_id": ride_request_id}
        update = {"$set": values}
        ride_data = ride_request.find_one(query)
        if ride_data is None:
            raise Exception("Invalid ride request id")

        ride_request.update_one(query, update)
