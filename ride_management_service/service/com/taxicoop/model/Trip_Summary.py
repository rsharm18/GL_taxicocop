from datetime import datetime

from com.taxicoop.model.Taxi import GeoData, Taxi_Type, Ride_Request_Status


class Trip_Summary:
    def __init__(self, user_id, taxi_id, latitude, longitude,
                 vehicle_type=Taxi_Type.DELUXE.value,
                 status=Ride_Request_Status.RIDE_COMPLETED):
        self.user_id = user_id
        self.taxi_id = taxi_id
        self.end_position = GeoData(longitude, latitude).__dict__
        self.status = status
        self.vehicle_type = vehicle_type
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
