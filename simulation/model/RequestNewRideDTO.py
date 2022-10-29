from enum import Enum


class Taxi_Type(Enum):
    UTILITY = "UTILITY"
    DELUXE = "DELUXE"
    LUXURY = "LUXURY"
    ECO = "ECO"
    ALL = "ALL"


class RequestNewRideDTO:
    def __init__(self, rider_id, start_longitude, start_latitude, destination_longitude, destination_latitude,
                 vehicle_type=Taxi_Type):
        self.rider_id = rider_id
        self.vehicle_type = vehicle_type
        self.start_longitude = start_longitude
        self.start_latitude = start_latitude
        self.destination_longitude = destination_longitude
        self.destination_latitude = destination_latitude
