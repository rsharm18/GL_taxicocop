import traceback
from os import getenv

from com.taxicoop.dto.RegisterNewLocationDTO import RegisterNewLocationDTO
from com.taxicoop.dto.RegisterNewTaxiDTO import RegisterNewTaxiDTO
from com.taxicoop.model.Location import Location
from com.taxicoop.model.Taxi import Taxi
from com.taxicoop.model.Taxi import Taxi_Type, GeoData
from com.taxicoop.service.DBHelper import DB_Helper
from com.taxicoop.model.Taxi import Taxi_Status
from com.taxicoop.dto.RequestBookTaxiDTO import RequestBookTaxiDTO

import requests
from dotenv import load_dotenv

load_dotenv()
# TAXI_BASE_URL = "http://taxicoop-api-load-balancer-898563336.us-east-1.elb.amazonaws.com/api/taxis/v1" #  getenv('TAXI_SERVICE_BASE_URL')
RIDE_REQUEST_SERVICE_BASE_URL = getenv('RIDE_REQUEST_SERVICE_BASE_URL', 'http://localhost:8080/api/rides/v1')

print(" RIDE_REQUEST_SERVICE_BASE_URL {}".format(RIDE_REQUEST_SERVICE_BASE_URL))


class Taxi_Service:

    def register_taxi(self, new_taxi: RegisterNewTaxiDTO) -> Taxi:
        new_taxi = Taxi(owner_name=new_taxi.name, owner_email=new_taxi.email, license_plate=new_taxi.license_plate,
                        longitude=new_taxi.longitude, latitude=new_taxi.latitude, type=new_taxi.vehicle_type)

        # TODO - do not allow adding a taxi for already registered user

        DB_Helper.register_taxi(new_taxi)
        return new_taxi

    def capture_location(self, new_taxi_location: RegisterNewLocationDTO):
        # TODO - check if taxi exists for a given taxi id

        final_location = Location(entity_id=new_taxi_location.entity_id, status=new_taxi_location.status,
                                  entity_type=new_taxi_location.entity_type, latitude=new_taxi_location.latitude,
                                  longitude=new_taxi_location.longitude, vehicle_type=new_taxi_location.vehicle_type)
        DB_Helper.publish_taxi_location(final_location)
        return "location for entity id = " + new_taxi_location.entity_id

    def get_nearby_taxis(self, user_latitude, user_longitude, vehicle_type=Taxi_Type.ALL):
        user_location = GeoData(user_longitude, user_latitude)
        return DB_Helper.get_near_by_taxis(user_location.__dict__, vehicle_type.value)

    def reserve(self, taxi_id, ride_req: RequestBookTaxiDTO):
        error = {'status': 'failed', 'message': 'Error confirming the ride'}
        print(" reserve taxi - START")
        try:

            taxis = DB_Helper.get_taxi_by_taxi_ids([taxi_id])
            if len(taxis) > 0:
                taxi = taxis[0]
                status = taxi['status']

                if not status == Taxi_Status.AVAILABLE.value:
                    return {'status': 'failed', 'message': 'Taxi is not available. The taxi is {}'.format(status)}

                url = '{}/{}/confirm_ride'.format(RIDE_REQUEST_SERVICE_BASE_URL, ride_req.ride_request_id)
                payload = {
                    'taxi_id': taxi_id,
                    'ride_request_id': ride_req.ride_request_id,
                    'vehicle_type': taxi['type']
                }

                print(" Calling Ride_Mgmt service  {} ".format(url))
                result = requests.post(url, json=payload).json()
                print("confirm_ride request response {}".format(result))
                if 'success' == result['status']:
                    DB_Helper.update_taxi(taxi_id, {'status': Taxi_Status.RIDE_IN_PROGRESS.value})
                    return {'status': 'success', 'message': 'Ride in Progress'}

                return {'status': 'failed', 'message': "ERROR :: {}".format(result['message'])}
            else:
                return error
        except Exception as ex:
            traceback.print_exc()
        return error

    def release(self, taxi_id):
        response = {'status': 'failed', 'message': 'Error fetching ride status'}
        print(" release taxi - START")
        try:

            taxis = DB_Helper.get_taxi_by_taxi_ids([taxi_id])
            if len(taxis) > 0:
                taxi = taxis[0]
                status = taxi['status']

                if not status == Taxi_Status.RIDE_IN_PROGRESS.value:
                    return {'status': 'failed', 'message': 'Taxi is available. The taxi is {}'.format(status)}

                DB_Helper.update_taxi(taxi_id, {'status': Taxi_Status.AVAILABLE.value})
                return {'status': 'success', 'message': 'Taxi is available'}
            else:
                return response
        except Exception as ex:
            traceback.print_exc()
        return response

    def get_all_taxis(self):
        taxis = DB_Helper.get_all_taxis()
        result = []
        for taxi in taxis:
            loc = taxi['location']
            coordinates = loc['coordinates']
            longitude = float(coordinates[0])
            latitude = float(coordinates[1])
            result.append(
                Taxi(owner_name=taxi['owner_name'], type=Taxi_Type[taxi['type']], owner_email=taxi['owner_email'],
                     license_plate=taxi['license_plate'], member_since=taxi['member_since'], taxi_id=taxi['taxi_id'],
                     status=Taxi_Status[taxi['status']],
                     longitude=longitude,
                     latitude=latitude
                     ).__dict__
            )

        return result

    def get_taxi_by_id(self, taxi_id):
        taxi = DB_Helper.get_taxi_by_id([taxi_id])
        result = []
        loc = taxi['location']
        coordinates = loc['coordinates']
        longitude = float(coordinates[0])
        latitude = float(coordinates[1])
        result.append(
            Taxi(owner_name=taxi['owner_name'], type=Taxi_Type[taxi['type']], owner_email=taxi['owner_email'],
                 license_plate=taxi['license_plate'], member_since=taxi['member_since'], taxi_id=taxi['taxi_id'],
                 status=Taxi_Status[taxi['status']],
                 longitude=longitude,
                 latitude=latitude
                 ).__dict__
        )
        return result
