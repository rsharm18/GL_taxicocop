import pprint

import pymongo
from bson import SON
from com.taxicoop.model.Location import Location
from com.taxicoop.model.Taxi import Taxi
from com.taxicoop.setup.Data_Generator import Data_Generator
from haversine import haversine, Unit

DEFINED_RADIUS = 5000

db_client = pymongo.MongoClient(
    "mongodb+srv://taxicoop:admin123@cluster0.ykco3.mongodb.net/?retryWrites=true&w=majority")

db = db_client.test
# Create a Database
taxi_mgmt_db = db_client['taxi_management']
# Create Collections
taxis = taxi_mgmt_db['taxis']
locations = taxi_mgmt_db['locations']

# Create Index(es)
locations.create_index([('position', pymongo.GEOSPHERE)])


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
        locations.insert_one(loc.__dict__)

    @staticmethod
    def get_all_taxis():
        return taxis.find()

    @staticmethod
    def get_locations_count():
        return locations.estimated_document_count()

    @staticmethod
    def get_near_by_taxis(user_location, vehicle_type):
        pprint.pprint("Location {}".format(user_location))
        print("Range \n")
        range_query = {'position': SON([("$near", user_location), ("$maxDistance", DEFINED_RADIUS)])}

        data = []
        loc1 = (user_location['coordinates'][1], user_location['coordinates'][0])
        for doc in locations.find(range_query):
            data.append(doc['entity_id'])
            position = doc['position']
            loc2 = (position['coordinates'][1], position['coordinates'][0])
            pprint.pprint("doc {} - distance {}".format(doc['entity_id'], haversine(loc1, loc2, Unit.KILOMETERS)))
            pprint.pprint(doc)

        # print("nearest \n")
        # nearest_query = {'position': {"$near": user_location}}
        # for doc in locations.find(nearest_query):
        #     position = doc['position']
        #     loc2 = (position['coordinates'][1], position['coordinates'][0])
        #
        #     pprint.pprint("doc {} - distance {}".format(doc['entity_id'], haversine(loc1, loc2, Unit.KILOMETERS)))

        return data
