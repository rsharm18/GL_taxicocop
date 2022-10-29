from pymongo import MongoClient, GEOSPHERE

from com.taxicoop.model.Ride_Request import Ride_Request
from com.taxicoop.model.Trip_Summary import NewTrip, CompleteTrip

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

    @staticmethod
    def get_all_rides():
        return ride_request.find()

    @staticmethod
    def get_ride_by_ride_request_id(ride_request_id):
        query = {"ride_request_id": ride_request_id}
        return ride_request.find_one(query)

    ## handle trip summary data
    @staticmethod
    def add_new_trip_summary(new_trip:NewTrip):
        query = {"ride_request_id": new_trip.ride_request_id}
        trip_data = trip_summary.find_one(query)
        if trip_data is not None:
            raise Exception("Duplicate Trip Data not allowed")

        trip_summary.insert_one(new_trip.__dict__)

    @staticmethod
    def complete_ride(complete_trip:CompleteTrip):
        query = {"ride_request_id": complete_trip.ride_request_id}
        update = {"$set": complete_trip.__dict__}
        trip_data = trip_summary.find_one(query)
        if trip_data is None:
            raise Exception("Invalid ride request id")

        trip_summary.update_one(query, update)

