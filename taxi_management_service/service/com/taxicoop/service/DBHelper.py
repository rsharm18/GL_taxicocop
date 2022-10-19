import pymongo

from taxi_management_service.service.com.taxicoop.model.Location import Location
from taxi_management_service.service.com.taxicoop.model.Taxi import Taxi
from taxi_management_service.service.com.taxicoop.setup.Data_Generator import Data_Generator

db_client = pymongo.MongoClient(
    "mongodb+srv://taxicoop:admin123@cluster0.ykco3.mongodb.net/?retryWrites=true&w=majority")

db = db_client.test
# Create a Database
taxi_mgmt_db = db_client['taxi_management']
# Create Collections
taxis = taxi_mgmt_db['taxis']
location = taxi_mgmt_db['location']


class DB_Helper:

    # db = client.test

    @staticmethod
    def configure_db():
        count = taxis.estimated_document_count()
        if count == 0:
            print("Adding dummy Data")
            data = Data_Generator.generate_taxi_data(50)
            taxis.insert_many(data)

    @staticmethod
    def register_taxi(taxi: Taxi):
        taxis.insert_one(taxi.__dict__)

    @staticmethod
    def publish_taxi_location(loc: Location):
        location.insert_one(loc.__dict__)

    @staticmethod
    def get_all_taxis():
        return taxis.find()
