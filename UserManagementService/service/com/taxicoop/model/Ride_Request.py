import uuid
from datetime import datetime
from enum import Enum


class GeoData:
    def __init__(self, longitude, latitude, type='Point'):
        self.coordinates = [longitude, latitude]
        self.type = type


class Taxi_Type(Enum):
    UTILITY = "UTILITY"
    DELUXE = "DELUXE"
    LUXURY = "LUXURY"
    ECO = "ECO"
    ALL = "ALL"


class Ride_Request_Status(Enum):
    RIDE_REQUESTED = "RIDE_REQUESTED"
    RIDE_SELECTED = "RIDE_SELECTED"
    RIDE_IN_PROGRESS = "RIDE_IN_PROGRESS"
    RIDE_COMPLETED = "RIDE_COMPLETED"
    RIDE_CANCELLED = "RIDE_CANCELLED"


class Ride_Request:
    def __init__(self, rider_id, longitude, latitude,
                 vehicle_type=Taxi_Type.DELUXE,
                 request_create_timestamp=datetime.now().isoformat(),
                 event_timestamp=datetime.now().isoformat(),
                 ride_request_id=str(uuid.uuid4()),
                 status: Ride_Request_Status = Ride_Request_Status.RIDE_REQUESTED):
        self.ride_request_id = ride_request_id
        self.vehicle_type = vehicle_type.value
        self.rider_id = rider_id
        self.ride_status = status.value
        self.request_create_timestamp = request_create_timestamp
        self.event_timestamp = event_timestamp
        self.near_by_taxis = []
        self.location = GeoData(longitude, latitude).__dict__
