from datetime import datetime

from com.taxicoop.model.Ride_Request import GeoData, Ride_Request_Status, Taxi_Type


class NewTrip:
    def __init__(self, ride_request_id, rider_id, taxi_id, start_longitude, start_latitude, destination_longitude,
                 destination_latitude, vehicle_type=Taxi_Type.ALL):
        self.ride_request_id = ride_request_id
        self.rider_id = rider_id
        self.taxi_id = taxi_id
        self.start_location = GeoData(start_longitude, start_latitude).__dict__
        self.end_location = GeoData(destination_longitude, destination_latitude).__dict__
        self.vehicle_type = vehicle_type.value
        self.trip_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.trip_status = Ride_Request_Status.RIDE_IN_PROGRESS.value


class CompleteTrip:
    def __init__(self, ride_request_id):
        self.ride_request_id = ride_request_id
        self.trip_end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.trip_status = Ride_Request_Status.RIDE_COMPLETED.value
