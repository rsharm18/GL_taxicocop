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
    id: str
    name: str
    type: Taxi_Type
    status: Taxi_Status
    member_since: str
    member_since: str

    def __init__(self, id, name, type: Taxi_Type, status: Taxi_Status, owner_email, member_since):
        self.id = id
        self.name = name
        self.type = type
        self.status = status
        self.member_since = member_since
        self.owner_email = owner_email
