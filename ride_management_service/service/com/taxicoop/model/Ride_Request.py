import uuid
from datetime import datetime
from enum import Enum


def transform_ride_db_data_to_model(ride_req):

    print(" ride_req {}".format(ride_req))

    loc = ride_req['start_location']
    coordinates = loc['coordinates']
    start_longitude = float(coordinates[0])
    start_latitude = float(coordinates[1])

    loc = ride_req['destination_location']
    coordinates = loc['coordinates']
    destination_longitude = float(coordinates[0])
    destination_latitude = float(coordinates[1])

    return Ride_Request(
        rider_id=ride_req['rider_id'],
        start_longitude=start_longitude,
        start_latitude=start_latitude,
        destination_longitude=destination_longitude,
        destination_latitude=destination_latitude,
        vehicle_type=Taxi_Type[ride_req['vehicle_type']],
        request_create_timestamp=ride_req['request_create_timestamp'],
        event_timestamp=ride_req['event_timestamp'],
        ride_request_id=ride_req['ride_request_id'],
        status=Ride_Request_Status[ride_req['ride_status']]
    )


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

    def __init__(self, rider_id, start_longitude, start_latitude, destination_longitude, destination_latitude,
                 vehicle_type=Taxi_Type.DELUXE,
                 request_create_timestamp=datetime.now().isoformat(),
                 event_timestamp=datetime.now().isoformat(),
                 ride_request_id=None,
                 status: Ride_Request_Status = Ride_Request_Status.RIDE_REQUESTED):
        self.ride_request_id = uuid.uuid4().hex if ride_request_id is None else ride_request_id
        self.vehicle_type = vehicle_type.value
        self.rider_id = rider_id
        self.ride_status = status.value
        self.request_create_timestamp = request_create_timestamp
        self.event_timestamp = event_timestamp
        self.near_by_taxis = []
        self.start_location = GeoData(start_longitude, start_latitude).__dict__
        self.destination_location = GeoData(destination_longitude, destination_latitude).__dict__


    def to_json(self):
        return {
            "ride_request_id": self.ride_request_id,
            "vehicle_type": self.vehicle_type,
            "rider_id": self.rider_id,
            "ride_status": self.ride_status,
            "request_create_timestamp": self.request_create_timestamp,
            "event_timestamp": self.event_timestamp,
            "near_by_taxis": self.near_by_taxis,
            "start_location": self.start_location,
            "destination_location": self.destination_location
        }
