from taxi_management_service.service.com.taxicoop.model.Taxi import Taxi_Type


class RegisterNewTaxiDto:
    name: str
    email: str
    vehicle_type: Taxi_Type
    license_plate: str

    def __init__(self, name, email, license_plate, vehicle_type: Taxi_Type = Taxi_Type.DELUXE):
        self.name = name
        self.email = email
        self.vehicle_type = vehicle_type
        self.license_plate = license_plate
