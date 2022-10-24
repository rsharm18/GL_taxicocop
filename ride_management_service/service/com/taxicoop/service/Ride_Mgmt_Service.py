import traceback
from os import getenv
from typing import Dict, Any

import requests
from dotenv import load_dotenv

from com.taxicoop.dto.ConfirmRideDTO import ConfirmRideDTO
from com.taxicoop.dto.RequestNewRideDTO import RequestNewRideDTO
from com.taxicoop.model.Ride_Request import Ride_Request, GeoData, Ride_Request_Status
from com.taxicoop.service.DBHelper import DB_Helper

## SEARCH RADIUS - 5KM
DEFINED_RADIUS = 5000

load_dotenv()
TAXI_BASE_URL = getenv('TAXI_SERVICE_BASE_URL')

print(" TAXI_BASE_URL {} ".format(TAXI_BASE_URL))
class Ride_Service:

    def request_ride(self, new_ride_request_dto: RequestNewRideDTO) -> Dict[str, Any]:
        new_ride_request = Ride_Request(rider_id=new_ride_request_dto.rider_id,
                                        longitude=new_ride_request_dto.longitude,
                                        latitude=new_ride_request_dto.latitude,
                                        vehicle_type=new_ride_request_dto.vehicle_type)

        # TODO - do not allow ride request if a ride is already in progress
        new_ride_request.near_by_taxis = self.__get_near_by_available_taxis__(new_ride_request.location,
                                                                              new_ride_request.vehicle_type)
        DB_Helper.register_new_ride_request(new_ride_request)
        return new_ride_request.to_json()

    def __get_near_by_available_taxis__(self, user_location, vehicle_type):
        # Getting all taxis within a certain distance range from a customer
        print('######################## ALL TAXIS WITHIN 5 KILOMETER ########################')

        url = '{}/nearby-taxis'.format(TAXI_BASE_URL)
        payload = {'longitude': user_location['coordinates'][0],
                   'latitude': user_location['coordinates'][1],
                   'vehicle_type': vehicle_type}

        print(" Calling taxi service  {}  with payload {} ".format(url,payload))
        result = requests.post(url, json=payload).json()

        print("response from taxi service = {}".format(result))

        return result
        # available_taxis =
        # range_query = {'location': SON([("$near", user_location), ("$maxDistance", DEFINED_RADIUS)])}
        # for doc in taxis.find(range_query):
        #     pprint.pprint(doc)

    def confirm_ride_request(self, confirm_ride: ConfirmRideDTO):
        error = {'status': 'failed',
                 'message': 'Error booking the ride. Please try again'}
        try:
            status = {'ride_status': Ride_Request_Status.RIDE_SELECTED.value}
            url = '{}/{}/book'.format(TAXI_BASE_URL, confirm_ride.taxi_id)
            payload = {}

            print(" Calling taxi service  {} ".format(url))
            result = requests.post(url, json=payload).json()

            print("Book Taxi Result {}".format(result))

            if not result['status'] == "success":
                return error
            print("response from taxi service = {}".format(result))
            DB_Helper.update_ride_request(confirm_ride.ride_request_id, status)
            return {'status': 'success',
                    'message': 'Successfully Booked the ride'}
        except Exception as ex:
            traceback.print_exc()

        return error
