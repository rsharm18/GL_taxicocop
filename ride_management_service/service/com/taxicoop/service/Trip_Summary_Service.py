from com.taxicoop.model.Ride_Request import Taxi_Type
from com.taxicoop.model.Trip_Summary import NewTrip, CompleteTrip
from com.taxicoop.service.DBHelper import DB_Helper


class Trip_Summary_Service:

    @staticmethod
    def start_trip(ride_req):
        # add the trip data to trip summary
        loc = ride_req['start_location']
        coordinates = loc['coordinates']
        start_longitude = float(coordinates[0])
        start_latitude = float(coordinates[1])

        loc = ride_req['destination_location']
        coordinates = loc['coordinates']
        destination_longitude = float(coordinates[0])
        destination_latitude = float(coordinates[1])

        DB_Helper.add_new_trip_summary(NewTrip(
            rider_id=ride_req['rider_id'],
            start_longitude=start_longitude,
            start_latitude=start_latitude,
            destination_longitude=destination_longitude,
            destination_latitude=destination_latitude,
            vehicle_type=Taxi_Type[ride_req['selected_vehicle_type']],
            ride_request_id=ride_req['ride_request_id'],
            taxi_id=ride_req['selected_taxi']
        ))

    @staticmethod
    def complete_trip(ride_request_id):
        complete_trip = CompleteTrip(ride_request_id)
        DB_Helper.complete_ride(complete_trip)
