from com.taxicoop.model.Ride_Request import Taxi_Type


class ConfirmRideDTO:
    def __init__(self, taxi_id, ride_request_id, vehicle_type: Taxi_Type):
        self.taxi_id = taxi_id
        self.ride_request_id = ride_request_id
        self.vehicle_type = vehicle_type.value
