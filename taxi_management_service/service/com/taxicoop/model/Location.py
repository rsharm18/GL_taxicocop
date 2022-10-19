from datetime import datetime

from taxi_management_service.service.com.taxicoop.model.Taxi import Taxi_Status, GeoData, Taxi_Type


class Location:
    def __init__(self, entity_id, entity_type, latitude, longitude,
                 vehicle_type: Taxi_Type = Taxi_Type.DELUXE,
                 status: Taxi_Status = Taxi_Status.AVAILABLE):
        self.entity_identity_id = entity_id
        self.entity_identity_type = entity_type
        self.position = GeoData.__init__(longitude, latitude).__dict__
        self.status = status.value
        self.vehicle_type = vehicle_type.value
        self.timestamp = datetime.now().timestamp()
