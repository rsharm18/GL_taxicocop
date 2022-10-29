from com.taxicoop.model.Ride_Request import Taxi_Type, Ride_Request_Status
from com.taxicoop.model.Trip_Summary import NewTrip, CompleteTrip, TripSummary
from com.taxicoop.service.DBHelper import DB_Helper


def transform_trip_db_data_to_model(trip_data):
    loc = trip_data['start_location']
    coordinates = loc['coordinates']
    start_longitude = float(coordinates[0])
    start_latitude = float(coordinates[1])

    loc = trip_data['end_location']
    coordinates = loc['coordinates']
    destination_longitude = float(coordinates[0])
    destination_latitude = float(coordinates[1])

    return TripSummary(
        rider_id=trip_data['rider_id'],
        start_longitude=start_longitude,
        start_latitude=start_latitude,
        destination_longitude=destination_longitude,
        destination_latitude=destination_latitude,
        vehicle_type=Taxi_Type[trip_data['vehicle_type']],
        trip_start_time=trip_data['trip_start_time'],
        trip_end_time=trip_data['trip_end_time'],
        ride_request_id=trip_data['ride_request_id'],
        trip_status=Ride_Request_Status[trip_data['trip_status']],
        taxi_id=trip_data['taxi_id']
    )


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

    @classmethod
    def get_all_trips(cls):
        trips = DB_Helper.get_all_trips()
        result = []
        for trip in trips:
            result.append(transform_trip_db_data_to_model(trip).__dict__)

        return result

    @staticmethod
    def get_trip_by_ride_request_id(ride_request_id):
        trip = DB_Helper.get_trip_by_ride_request_id(ride_request_id)
        if trip is None:
            return {}
        else:
            return transform_trip_db_data_to_model(trip).__dict__
