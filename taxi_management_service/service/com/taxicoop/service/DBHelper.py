import pymongo

from taxi_management_service.service.com.taxicoop.model.Taxi import Taxi
from taxi_management_service.service.com.taxicoop.setup.Data_Generator import Data_Generator

db_client = pymongo.MongoClient(
    "mongodb+srv://taxicoop:admin123@cluster0.ykco3.mongodb.net/?retryWrites=true&w=majority")

db = db_client.test
# Create a Database
aggregator_db = db_client['taxi_management']
# Create Collections
taxis = aggregator_db['taxis']


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
