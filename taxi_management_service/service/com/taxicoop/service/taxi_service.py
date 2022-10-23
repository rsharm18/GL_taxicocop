import traceback

from com.taxicoop.dto.RegisterNewLocationDTO import RegisterNewLocationDTO
from com.taxicoop.dto.RegisterNewTaxiDTO import RegisterNewTaxiDTO
from com.taxicoop.model.Location import Location
from com.taxicoop.model.Taxi import Taxi
from com.taxicoop.model.Taxi import Taxi_Type, GeoData
from com.taxicoop.service.DBHelper import DB_Helper
from taxicoop.model.Taxi import Taxi_Status

class Taxi_Service:

    def register_taxi(self, new_taxi: RegisterNewTaxiDTO) -> Taxi:
        new_taxi = Taxi(owner_name=new_taxi.name,
                        owner_email=new_taxi.email,
                        license_plate=new_taxi.license_plate,
                        longitude=new_taxi.longitude,
                        latitude=new_taxi.latitude,
                        type=new_taxi.vehicle_type)

        # TODO - do not allow adding a taxi for already registered user

        DB_Helper.register_taxi(new_taxi)
        return new_taxi

    def capture_location(self, new_taxi_location: RegisterNewLocationDTO):
        # TODO - check if taxi exists for a given taxi id

        final_location = Location(entity_id=new_taxi_location.entity_id,
                                  status=new_taxi_location.status,
                                  entity_type=new_taxi_location.entity_type,
                                  latitude=new_taxi_location.latitude,
                                  longitude=new_taxi_location.longitude,
                                  vehicle_type=new_taxi_location.vehicle_type
                                  )
        DB_Helper.publish_taxi_location(final_location)
        return "location for entity id = " + new_taxi_location.entity_id

    def get_nearby_taxis(self, user_latitude, user_longitude, vehicle_type=Taxi_Type.ALL):
        user_location = GeoData(user_longitude, user_latitude)
        return DB_Helper.get_near_by_taxis(user_location.__dict__, vehicle_type.value)

    def reserve(self, taxi_id):
        error = {'status': 'failed', 'message': 'Error confirming the ride'}
        print(" reserve taxi - START")
        try:

            taxis = DB_Helper.get_taxi_by_taxi_ids([taxi_id])
            if len(taxis) > 0:
                taxi = taxis[0]
                status = taxi['status']

                if not status == Taxi_Status.AVAILABLE.value:
                    return {'status': 'failed', 'message': 'Taxi is not available. The taxi is {}'.format(status)}

                DB_Helper.update_taxi(taxi_id, {'status': Taxi_Status.RIDE_IN_PROGRESS.value})
                return {'status': 'success', 'message': 'Ride in Progress'}
            else:
                return error
        except Exception as ex:
            traceback.print_exc()
        return error
