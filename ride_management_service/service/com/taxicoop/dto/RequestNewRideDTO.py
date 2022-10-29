from com.taxicoop.model.Ride_Request import Taxi_Type


class RequestNewRideDTO:
    def __init__(self, rider_id, start_longitude, start_latitude,destination_longitude,destination_latitude,
                 vehicle_type=Taxi_Type):
        self.rider_id = rider_id
        self.vehicle_type = vehicle_type
        self.start_longitude = start_longitude
        self.start_latitude = start_latitude
        self.destination_longitude = destination_longitude
        self.destination_latitude = destination_latitude
