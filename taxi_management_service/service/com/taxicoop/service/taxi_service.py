from com.taxicoop.dto.RegisterNewLocationDTO import RegisterNewLocationDTO
from com.taxicoop.dto.RegisterNewTaxiDTO import RegisterNewTaxiDTO
from com.taxicoop.model.Location import Location
from com.taxicoop.model.Taxi import Taxi
from com.taxicoop.service.DBHelper import DB_Helper


class Taxi_Service:

    def register_taxi(self, new_taxi: RegisterNewTaxiDTO) -> Taxi:
        new_taxi = Taxi(user_name=new_taxi.name,
                        owner_email=new_taxi.email,
                        license_plate=new_taxi.license_plate,
                        longitude=new_taxi.longitude,
                        latitude=new_taxi.longitude,
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
