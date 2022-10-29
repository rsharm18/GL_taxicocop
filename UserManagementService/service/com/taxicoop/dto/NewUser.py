#from com.taxicoop.model.Taxi import Taxi_Type


class RegisterNewUserDTO:
    name: str
    email: str
    contact_number: str
    longitude: float
    latitude: float
    status : str

    def __init__(self, name, email, contact_number, longitude, latitude, status):
        self.name = name
        self.email = email
        self.contact_number = contact_number
        self.longitude = longitude
        self.latitude = latitude
        self.status = status

