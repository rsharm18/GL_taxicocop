from taxi_management_service.service.com.taxicoop.model.Taxi import Taxi_Type, Taxi_Status


class RegisterNewLocationDTO:
    def __init__(self, entity_id, entity_type, latitude, longitude,
                 vehicle_type=Taxi_Type.DELUXE.value,
                 status=Taxi_Status.AVAILABLE.value):
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.latitude = latitude
        self.longitude = longitude
        self.status = status
        self.vehicle_type = vehicle_type
