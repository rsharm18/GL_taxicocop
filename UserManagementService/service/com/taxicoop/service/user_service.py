import traceback

from com.taxicoop.dto.RegisterNewLocationDTO import RegisterNewLocationDTO
from com.taxicoop.dto.RegisterNewTaxiDTO import RegisterNewTaxiDTO
from com.taxicoop.model.Location import Location
from com.taxicoop.model.Taxi import Taxi
from com.taxicoop.model.Taxi import Taxi_Type, GeoData
from com.taxicoop.service.DBHelper import DB_Helper
from com.taxicoop.model.Taxi import Taxi_Status


class User_Service:

    def register_user(self, new_taxi: RegisterNewTaxiDTO) -> Taxi:
        new_taxi = Taxi(owner_name=new_taxi.name, owner_email=new_taxi.email, license_plate=new_taxi.license_plate,
                        longitude=new_taxi.longitude, latitude=new_taxi.latitude, type=new_taxi.vehicle_type)

        # TODO - do not allow adding a taxi for already registered user

        DB_Helper.register_taxi(new_taxi)
        return new_taxi



    def get_all_Users(self):
        users = DB_Helper.get_all_users()
        result = []
        for user in users:
            name = users['name']
            email = users['email']
            contact_number = users['contact_number']

            result.append(
                Taxi(owner_name=taxi['owner_name'], type=Taxi_Type[taxi['type']], owner_email=taxi['owner_email'],
                     license_plate=taxi['license_plate'], member_since=taxi['member_since'], taxi_id=taxi['taxi_id'],
                     status=Taxi_Status[taxi['status']],
                     longitude=longitude,
                     latitude=latitude
                     ).__dict__
            )

        return result
