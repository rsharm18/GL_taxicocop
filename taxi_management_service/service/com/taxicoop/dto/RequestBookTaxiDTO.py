class RequestBookTaxiDTO:
    def __init__(self, taxi_id, start_location, destination_location, ride_request_id):
        self.taxi_id = taxi_id
        self.start_location = start_location
        self.destination_location = destination_location
        self.ride_request_id = ride_request_id
