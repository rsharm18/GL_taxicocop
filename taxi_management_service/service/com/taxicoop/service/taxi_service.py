from taxi_management_service.service.com.taxicoop.dto.RegisterNewTaxiDTO import RegisterNewTaxiDto
from taxi_management_service.service.com.taxicoop.model.Taxi import Taxi
from taxi_management_service.service.com.taxicoop.service.DBHelper import DB_Helper


class Taxi_Service:

    def register_taxi(self, new_taxi: RegisterNewTaxiDto) -> Taxi:
        new_taxi = Taxi(user_name=new_taxi.name,
                        owner_email=new_taxi.email,
                        license_plate=new_taxi.license_plate,
                        type=new_taxi.vehicle_type)

        # TODO - do not allow adding a taxi for already registered user

        DB_Helper.register_taxi(new_taxi)
        return new_taxi

    def capture_location(self, taxi_id):
        return "location for taxi_id = " + taxi_id
