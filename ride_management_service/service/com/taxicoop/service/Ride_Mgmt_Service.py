from os import getenv

import requests
from com.taxicoop.dto.RequestNewRideDTO import RequestNewRideDTO
from com.taxicoop.model.Ride_Request import Ride_Request, GeoData
from com.taxicoop.service.DBHelper import DB_Helper
from dotenv import load_dotenv

## SEARCH RADIUS - 5KM
DEFINED_RADIUS = 5000

load_dotenv()
TAXI_BASE_URL = getenv('TAXI_SERVICE_BASE_URL')


class Ride_Service:

    def request_ride(self, new_ride_request_dto: RequestNewRideDTO) -> Ride_Request:
        new_ride_request = Ride_Request(rider_id=new_ride_request_dto.rider_id,
                                        longitude=new_ride_request_dto.longitude,
                                        latitude=new_ride_request_dto.longitude,
                                        vehicle_type=new_ride_request_dto.vehicle_type)

        # TODO - do not allow ride request if a ride is already in progress

        DB_Helper.register_new_ride_request(new_ride_request)
        self.__get_near_by_available_taxis__(new_ride_request.location)
        return new_ride_request

    def __get_near_by_available_taxis__(self, user_location: GeoData):
        # Getting all taxis within a certain distance range from a customer
        print('######################## ALL TAXIS WITHIN 5 KILOMETER ########################')

        url = '{}/nearby-taxis'.format(TAXI_BASE_URL)
        print("url {}".format(url))
        payload = {'longitude': user_location['coordinates'][0],
                   'latitude': user_location['coordinates'][1]}

        x = requests.post(url, json=payload)

        print("x = {}".format(x))
        # available_taxis =
        # range_query = {'location': SON([("$near", user_location), ("$maxDistance", DEFINED_RADIUS)])}
        # for doc in taxis.find(range_query):
        #     pprint.pprint(doc)
