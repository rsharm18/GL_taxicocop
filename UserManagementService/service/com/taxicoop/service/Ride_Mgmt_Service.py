from com.taxicoop.service.DBHelper import DB_Helper

from ride_management_service.service.com.taxicoop.dto.RequestNewRideDTO import RequestNewRideDTO
from ride_management_service.service.com.taxicoop.model.Ride_Request import Ride_Request


class Ride_Service:

    def request_ride(self, new_ride_request_dto: RequestNewRideDTO) -> Ride_Request:
        new_ride_request = Ride_Request(rider_id=new_ride_request_dto.rider_id,
                                        longitude=new_ride_request_dto.longitude,
                                        latitude=new_ride_request_dto.longitude,
                                        vehicle_type=new_ride_request_dto.vehicle_type)

        # TODO - do not allow ride request if a ride is already in progress

        DB_Helper.register_new_ride_request(new_ride_request)

        return new_ride_request
