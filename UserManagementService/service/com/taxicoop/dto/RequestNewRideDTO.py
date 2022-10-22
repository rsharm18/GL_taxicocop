from com.taxicoop.model.Ride_Request import Taxi_Type


class RequestNewRideDTO:
    def __init__(self, rider_id, longitude, latitude,
                 vehicle_type=Taxi_Type):
        self.rider_id = rider_id
        self.vehicle_type = vehicle_type
        self.longitude = longitude
        self.latitude = latitude
