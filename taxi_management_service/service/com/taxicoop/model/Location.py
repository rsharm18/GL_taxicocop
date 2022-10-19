from datetime import datetime

from taxi_management_service.service.com.taxicoop.model.Taxi import Taxi_Status, GeoData, Taxi_Type


class Location:
    def __init__(self, entity_id, entity_type, latitude, longitude,
                 vehicle_type=Taxi_Type.DELUXE.value,
                 status=Taxi_Status.AVAILABLE.value):
        self.entity_identity_id = entity_id
        self.entity_identity_type = entity_type
        self.position = GeoData(longitude, latitude).__dict__
        self.status = status
        self.vehicle_type = vehicle_type
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
