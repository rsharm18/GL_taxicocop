import uuid
from datetime import datetime
from enum import Enum


class Taxi_Type(Enum):
    UTILITY = "UTILITY"
    DELUXE = "DELUXE"
    LUXURY = "LUXURY"
    ECO = "ECO"


class Taxi_Status(Enum):
    AVAILABLE = "AVAILABLE"
    RIDE_IN_PROGRESS = "RIDE_IN_PROGRESS"
    BLOCKED = "BLOCKED"


class Taxi:
    taxi_id: str
    user_name: str
    type: Taxi_Type
    status: Taxi_Status
    owner_email: str
    member_since: str
    license_plate: str

    def __init__(self, user_name, type: Taxi_Type, owner_email, license_plate,
                 member_since=datetime.now().isoformat(),
                 taxi_id=str(uuid.uuid4()),
                 status: Taxi_Status = Taxi_Status.AVAILABLE):
        self.taxi_id = taxi_id
        self.user_name = user_name
        self.type = type.value
        self.status = status.value
        self.member_since = member_since
        self.owner_email = owner_email
        self.license_plate = license_plate
