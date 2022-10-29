from enum import Enum


class Taxi_Type(Enum):
    UTILITY = "UTILITY"
    DELUXE = "DELUXE"
    LUXURY = "LUXURY"
    ECO = "ECO"
    ALL = "ALL"


class RegisterNewTaxiDTO:
    name: str
    email: str
    vehicle_type: Taxi_Type
    license_plate: str
    longitude: float
    latitude: float

    def __init__(self, name, email, license_plate, longitude, latitude, vehicle_type: Taxi_Type = Taxi_Type.DELUXE):
        self.name = name
        self.email = email
        self.vehicle_type = vehicle_type.value
        self.license_plate = license_plate
        self.longitude = longitude
        self.latitude = latitude
