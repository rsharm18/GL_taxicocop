import traceback
from os import getenv
from typing import Dict, Any

import requests
from dotenv import load_dotenv

from com.taxicoop.dto.ConfirmRideDTO import ConfirmRideDTO
from com.taxicoop.dto.RequestNewRideDTO import RequestNewRideDTO
from com.taxicoop.model.Ride_Request import Ride_Request, Ride_Request_Status, Taxi_Type, \
    transform_ride_db_data_to_model
from com.taxicoop.service.DBHelper import DB_Helper
from com.taxicoop.service.RideReq_To_Nearby_Taxi_Helper import send_ride_request_to_nearby_taxis
from com.taxicoop.service.Trip_Summary_Service import Trip_Summary_Service

load_dotenv()
TAXI_BASE_URL = getenv('TAXI_SERVICE_BASE_URL', 'http://localhost:8081/api/taxis/v1/')

STARTING_LONGITUDE = getenv('STARTING_LONGITUDE', 88.358536)
ENDING_LONGITUDE = getenv('ENDING_LONGITUDE', 90.358536)

STARTING_LATITUDE = getenv('STARTING_LATITUDE', 22.578005)
ENDING_LATITUDE = getenv('ENDING_LATITUDE', 23.578005)

print(" TAXI_BASE_URL {} ".format(TAXI_BASE_URL))


class Ride_Service:

    def get_ride_request_by_id(self, ride_request_id):
        ride_request = DB_Helper.get_ride_by_ride_request_id(ride_request_id)
        if ride_request is None:
            return {}

        return transform_ride_db_data_to_model(ride_request).__dict__

    def get_all_ride_requests(self):
        ride_requests = DB_Helper.get_all_rides()
        result = []
        for ride_req in ride_requests:
            result.append(transform_ride_db_data_to_model(ride_req).__dict__)
        return result

    def request_ride(self, new_ride_request_dto: RequestNewRideDTO) -> Dict[str, Any]:

        # check if the user's starting location is in the range
        if not self.__is_req_in_range__(new_ride_request_dto.start_longitude, new_ride_request_dto.start_latitude):
            return {
                'status': "FAILED",
                'message': 'User is out of the service area'
            }

        if not self.__is_req_in_range__(new_ride_request_dto.destination_longitude,
                                        new_ride_request_dto.destination_latitude):
            return {
                'status': "FAILED",
                'message': 'User destination is out of the service area'
            }

        new_ride_request = Ride_Request(rider_id=new_ride_request_dto.rider_id,
                                        start_longitude=new_ride_request_dto.start_longitude,
                                        start_latitude=new_ride_request_dto.start_latitude,
                                        destination_longitude=new_ride_request_dto.destination_longitude,
                                        destination_latitude=new_ride_request_dto.destination_latitude,
                                        vehicle_type=new_ride_request_dto.vehicle_type)

        new_ride_request.near_by_taxis = self.__get_near_by_available_taxis__(new_ride_request.start_location,
                                                                              new_ride_request.vehicle_type)
        DB_Helper.register_new_ride_request(new_ride_request)
        send_ride_request_to_nearby_taxis(new_ride_request)
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

    def confirm_ride_request(self, confirm_ride: ConfirmRideDTO):

        print("Confirming Ride Request {}".format(confirm_ride))

        response = {'status': 'failed',
                    'message': 'Error booking the ride. Please try again'}
        try:
            data = {
                'ride_status': Ride_Request_Status.RIDE_SELECTED.value,
                'selected_taxi': confirm_ride.taxi_id,
                'selected_vehicle_type': confirm_ride.vehicle_type
            }

            ride_req = transform_ride_db_data_to_model(
                DB_Helper.get_ride_by_ride_request_id(confirm_ride.ride_request_id))
            print(ride_req.__dict__)
            print(
                " ride_req.ride_status= {} , {} , ride_req.ride_status == Ride_Request_Status.RIDE_REQUESTED.value = {}".format(
                    ride_req.ride_status, Ride_Request_Status.RIDE_REQUESTED.value,
                    ride_req.ride_status == Ride_Request_Status.RIDE_REQUESTED.value))

            if ride_req.ride_status == Ride_Request_Status.RIDE_REQUESTED.value:
                DB_Helper.update_ride_request(confirm_ride.ride_request_id, data)
                return {'status': 'success',
                        'message': 'Successfully Booked the ride'}

            return {'status': 'failed',
                    'message': 'ERROR : ride is already booked. Current ride status {}'.format(ride_req.ride_status)}

        except Exception as ex:
            traceback.print_exc()

        return response

    def complete_ride_request(self, ride_request_id):
        response = {'status': 'failed',
                    'message': 'Error Completing the ride. Please try again'}
        try:
            status = {'ride_status': Ride_Request_Status.RIDE_COMPLETED.value}

            ride_req_db_data = DB_Helper.get_ride_by_ride_request_id(ride_request_id)
            ride_req = transform_ride_db_data_to_model(ride_req_db_data)

            print("TAXI_BASE_URL = {} , ride_req.selected_taxi= {}".format(TAXI_BASE_URL, ride_req.selected_taxi))
            url = '{}/{}/complete'.format(TAXI_BASE_URL, ride_req.selected_taxi)
            payload = {}

            print(" Calling taxi service  {} ".format(url))
            result = requests.post(url, json=payload).json()

            print("Complete Taxi Result {}".format(result))

            if not result['status'] == "success":
                response['message'] = result['message']
                return response

            print("response from taxi service = {}".format(result))

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
        print("ride_req ".format(ride_req))
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

    def __is_req_in_range__(self, req_long, req_lat):
        if not (STARTING_LONGITUDE <= req_long <= ENDING_LONGITUDE):
            return False

        if not (STARTING_LATITUDE <= req_lat <= ENDING_LATITUDE):
            return False

        return True
