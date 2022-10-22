import pprint

import pymongo
from bson import SON
from com.taxicoop.model.Location import Location
from com.taxicoop.model.Taxi import Taxi
from com.taxicoop.setup.Data_Generator import Data_Generator
from haversine import haversine, Unit

from taxi_management_service.service.com.taxicoop.dto.NearByTaxiDTO import NearByTaxis

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
    def get_taxi_by_taxi_id(taxi_ids=None):
        if taxi_ids is None:
            return []

        print("taxi_ids {}".format(taxi_ids))
        near_by_taxis = []
        for taxi in taxis.find({'taxi_id': {'$in': taxi_ids}}):
            near_by_taxis.append(taxi)
        return near_by_taxis

    @staticmethod
    def get_near_by_taxis(user_location, vehicle_type):
        # pprint.pprint("Location {}".format(user_location))
        print("Range \n")
        range_query = {'position': SON([("$near", user_location), ("$maxDistance", DEFINED_RADIUS)])}

        data = []
        loc1 = (user_location['coordinates'][1], user_location['coordinates'][0])
        taxi_locations = {}
        query_taxi_ids = []
        for doc in locations.find(range_query).limit(5):
            data.append(doc['entity_id'])
            position = doc['position']
            loc2 = (position['coordinates'][1], position['coordinates'][0])
            doc['distance'] = haversine(loc1, loc2, Unit.KILOMETERS)
            # pprint.pprint("doc {} - distance {}".format(doc['entity_id'], haversine(loc1, loc2, Unit.KILOMETERS)))
            taxi_locations[doc['entity_id']] = doc
            query_taxi_ids.append(doc['entity_id'])

        # pprint.pprint("query_taxi_ids : {}".format(query_taxi_ids))

        taxi_data = DB_Helper.get_taxi_by_taxi_id(query_taxi_ids)
        result = []
        for taxi_info in taxi_data:
            location = taxi_locations.get(taxi_info['taxi_id'])
            result.append(NearByTaxis(taxi_id=taxi_info['taxi_id'],
                                      owner_name=taxi_info['user_name'],
                                      vehicle_type=taxi_info['type'],
                                      vehicle_status=taxi_info['status'],
                                      member_since=taxi_info['member_since'],
                                      license_plate=taxi_info['license_plate'],
                                      distance=location['distance'],
                                      taxi_location=location['position']['coordinates']
                                      ).__dict__)

        # print("nearest \n")
        # nearest_query = {'position': {"$near": user_location}}
        # for doc in locations.find(nearest_query):
        #     position = doc['position']
        #     loc2 = (position['coordinates'][1], position['coordinates'][0])
        #
        #     pprint.pprint("doc {} - distance {}".format(doc['entity_id'], haversine(loc1, loc2, Unit.KILOMETERS)))

        pprint.pprint(" result {}".format(result))
        return result
