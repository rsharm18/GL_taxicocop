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
    ALL = "ALL"  ## query all taxi types


class Taxi_Status(Enum):
    AVAILABLE = "AVAILABLE"
    RIDE_ACCEPTED = "RIDE_ACCEPTED"
    RIDE_IN_PROGRESS = "RIDE_IN_PROGRESS"
    BLOCKED = "BLOCKED"


class Taxi:
    def __init__(self, owner_name, type: Taxi_Type, owner_email, license_plate,
                 longitude, latitude,
                 member_since=datetime.now().isoformat(),
                 taxi_id=None,
                 status: Taxi_Status = Taxi_Status.AVAILABLE):
        self.taxi_id = uuid.uuid4().hex if taxi_id is not None else taxi_id
        self.owner_name = owner_name
        self.type = type.value
        self.status = status.value
        self.member_since = member_since
        self.owner_email = owner_email
        self.license_plate = license_plate
        self.location = GeoData(longitude, latitude).__dict__
