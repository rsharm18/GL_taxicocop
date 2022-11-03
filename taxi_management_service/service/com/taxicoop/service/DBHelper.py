import pprint
from datetime import datetime, timedelta

import pymongo
import certifi
from bson import SON
from haversine import haversine, Unit

from com.taxicoop.dto.NearByTaxiDTO import NearByTaxis
from com.taxicoop.model.Location import Location
from com.taxicoop.model.Taxi import Taxi
from com.taxicoop.model.Taxi import Taxi_Type, Taxi_Status

DEFINED_RADIUS = 5000


db_client = pymongo.MongoClient(
    "mongodb+srv://taxicoop:admin123@cluster0.ykco3.mongodb.net/?retryWrites=true&w=majority",
     tlsCAFile=certifi.where()
)

db = db_client.test
# Create a Database
taxi_mgmt_db = db_client['taxi_management']
# Create Collections
taxis = taxi_mgmt_db['taxis']
locations = taxi_mgmt_db['locations']

max_allowed_minutes_range_data = 2
max_minutes_stale_data = 5

# Create Index(es)
locations.create_index([('position', pymongo.GEOSPHERE)])


class DB_Helper:

    # db = client.test

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
    def get_taxi_by_taxi_ids(taxi_ids=None):
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

        from_range = datetime.today() - timedelta(minutes=max_allowed_minutes_range_data)

        print("from_range {}".format(from_range))

        criteria = [{'position': SON([("$near", user_location), ("$maxDistance", DEFINED_RADIUS)])},
                    {"timestamp": {"$gte": from_range}}]

        if not Taxi_Type.ALL.value == vehicle_type:
            criteria.append({"vehicle_type": vehicle_type})

        range_query = {
            "$and": criteria
        }

        print("range_query {}".format(range_query))
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

        taxi_data = DB_Helper.get_taxi_by_taxi_ids(query_taxi_ids)
        result = []
        pprint.pprint(" taxi_locations {}".format(taxi_locations))
        for taxi_info in taxi_data:

            if not taxi_info["status"] == Taxi_Status.AVAILABLE.value:
                continue

            location = taxi_locations.get(taxi_info['taxi_id'])
            result.append(NearByTaxis(taxi_id=taxi_info['taxi_id'],
                                      owner_name=taxi_info['owner_name'],
                                      vehicle_type=taxi_info['type'],
                                      vehicle_status=taxi_info['status'],
                                      member_since=taxi_info['member_since'],
                                      license_plate=taxi_info['license_plate'],
                                      distance=location['distance'],
                                      taxi_location=location['position']['coordinates']
                                      ).__dict__)

        pprint.pprint(" result {}".format(result))
        return result

    @staticmethod
    def delete_stale_data():
        from_range = datetime.today() - timedelta(minutes=max_minutes_stale_data)

        print("from_range {}".format(from_range))

        criteria = {"timestamp": {"$lte": from_range}}
        locations.delete_many(criteria)

    @staticmethod
    def update_taxi(taxi_id, values):
        query = {"taxi_id": taxi_id}
        update = {"$set": values}
        taxi_data = taxis.find_one(query)
        if taxi_data is None:
            raise Exception("Invalid Taxi id")

        taxis.update_one(query, update)

    @staticmethod
    def get_taxi_by_id(taxi_id):
        print("taxi_id {}".format(taxi_id))
        taxi_data = taxis.find(taxi_id)
        if taxi_data is None:
            raise Exception("Invalid Taxi id")
        return taxi_data
