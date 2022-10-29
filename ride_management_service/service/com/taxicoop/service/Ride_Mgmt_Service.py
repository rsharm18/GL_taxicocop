import traceback
from os import getenv
from typing import Dict, Any

import requests
from dotenv import load_dotenv

from com.taxicoop.dto.ConfirmRideDTO import ConfirmRideDTO
from com.taxicoop.dto.RequestNewRideDTO import RequestNewRideDTO
from com.taxicoop.model.Ride_Request import Ride_Request, Ride_Request_Status, Taxi_Type
from com.taxicoop.service.DBHelper import DB_Helper
## SEARCH RADIUS - 5KM
from com.taxicoop.service.Trip_Summary_Service import Trip_Summary_Service

DEFINED_RADIUS = 5000

load_dotenv()
TAXI_BASE_URL = getenv('TAXI_SERVICE_BASE_URL')

print(" TAXI_BASE_URL {} ".format(TAXI_BASE_URL))


class Ride_Service:

    def request_ride(self, new_ride_request_dto: RequestNewRideDTO) -> Dict[str, Any]:
        new_ride_request = Ride_Request(rider_id=new_ride_request_dto.rider_id,
                                        start_longitude=new_ride_request_dto.start_longitude,
                                        start_latitude=new_ride_request_dto.start_latitude,
                                        destination_longitude=new_ride_request_dto.destination_longitude,
                                        destination_latitude=new_ride_request_dto.destination_latitude,
                                        vehicle_type=new_ride_request_dto.vehicle_type)

        # TODO - do not allow ride request if a ride is already in progress
        new_ride_request.near_by_taxis = self.__get_near_by_available_taxis__(new_ride_request.start_location,
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

        print(" Calling taxi service  {}  with payload {} ".format(url, payload))
        result = requests.post(url, json=payload).json()

        print("response from taxi service = {}".format(result))

        return result
        # available_taxis =
        # range_query = {'location': SON([("$near", user_location), ("$maxDistance", DEFINED_RADIUS)])}
        # for doc in taxis.find(range_query):
        #     pprint.pprint(doc)

    def confirm_ride_request(self, confirm_ride: ConfirmRideDTO):
        response = {'status': 'failed',
                    'message': 'Error booking the ride. Please try again'}
        try:
            data = {
                'ride_status': Ride_Request_Status.RIDE_SELECTED.value,
                'selected_taxi': confirm_ride.taxi_id,
                'selected_vehicle_type': confirm_ride.vehicle_type
            }
            url = '{}/{}/book'.format(TAXI_BASE_URL, confirm_ride.taxi_id)
            payload = {}

            print(" Calling taxi service  {} ".format(url))
            result = requests.post(url, json=payload).json()

            print("Book Taxi Result {}".format(result))

            if not result['status'] == "success":
                response['message'] = result['message']
                return response
            print("response from taxi service = {}".format(result))
            DB_Helper.update_ride_request(confirm_ride.ride_request_id, data)
            return {'status': 'success',
                    'message': 'Successfully Booked the ride'}
        except Exception as ex:
            traceback.print_exc()

        return response

    def get_all_ride_requests(self):
        ride_requests = DB_Helper.get_all_rides()
        result = []
        for ride_req in ride_requests:
            loc = ride_req['start_location']
            coordinates = loc['coordinates']
            start_longitude = float(coordinates[0])
            start_latitude = float(coordinates[1])

            loc = ride_req['destination_location']
            coordinates = loc['coordinates']
            destination_longitude = float(coordinates[0])
            destination_latitude = float(coordinates[1])
            result.append(Ride_Request(
                rider_id=ride_req['rider_id'],
                start_longitude=start_longitude,
                start_latitude=start_latitude,
                destination_longitude=destination_longitude,
                destination_latitude=destination_latitude,
                vehicle_type=Taxi_Type[ride_req['vehicle_type']],
                request_create_timestamp=ride_req['request_create_timestamp'],
                event_timestamp=ride_req['event_timestamp'],
                ride_request_id=ride_req['ride_request_id'],
                status=Ride_Request_Status[ride_req['status']]
            ).__dict__)
        return result

    def complete_ride_request(self, ride_request_id):
        response = {'status': 'failed',
                    'message': 'Error Completing the ride. Please try again'}
        try:
            status = {'ride_status': Ride_Request_Status.RIDE_COMPLETED.value}

            # TODO - uncomment this to release taxi
            # url = '{}/{}/complete'.format(TAXI_BASE_URL, complete_ride.taxi_id)
            # payload = {}
            #
            # print(" Calling taxi service  {} ".format(url))
            # result = requests.post(url, json=payload).json()
            #
            # print("Complete Taxi Result {}".format(result))
            #
            # if not result['status'] == "success":
            #     return response
            # print("response from taxi service = {}".format(result))

            DB_Helper.update_ride_request(ride_request_id, status)
            Trip_Summary_Service.complete_trip(ride_request_id)
            return {'status': 'success',
                    'message': 'Successfully completed the ride'}
        except Exception as ex:
            traceback.print_exc()

        return response

    def start_trip(self, ride_request_id):
        response = {'status': 'success',
                    'message': 'Trip Started!'}
        # get ride request data
        ride_req = DB_Helper.get_ride_by_ride_request_id(ride_request_id)
        if ride_req is None:
            response['message'] = 'Invalid ride id'
            response['status'] = 'failed'
            return response

        # set the ride status to ride in progress
        status = {'ride_status': Ride_Request_Status.RIDE_IN_PROGRESS.value}
        DB_Helper.update_ride_request(ride_request_id, status)

        # add the trip data to trip summary
        try:
            Trip_Summary_Service.start_trip(ride_req)
        except Exception as ex:
            response['message'] = "Invalid Trip Data"
            response['status'] = 'failed'
            return response

        return response
