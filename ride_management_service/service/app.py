import traceback

from flask import Flask, request
from flask_cors import CORS

from com.taxicoop.dto.ConfirmRideDTO import ConfirmRideDTO
from com.taxicoop.dto.RequestNewRideDTO import RequestNewRideDTO
from com.taxicoop.model.Ride_Request import Taxi_Type
from com.taxicoop.service.Ride_Mgmt_Service import Ride_Service
from com.taxicoop.service.Trip_Summary_Service import Trip_Summary_Service

app = Flask(__name__)
CORS(app)

service = Ride_Service()

mandatory_new_ride_request_fields = {'rider_id', 'start_longitude', 'start_latitude', 'destination_longitude',
                                     'destination_latitude'}
mandatory_confirm_ride_fields = {'taxi_id', 'vehicle_type'}


@app.route("/api/rides/v1", methods=["GET"])
def get_all_ride_requests():
    return service.get_all_ride_requests()


@app.route("/api/rides/v1/<string:ride_request_id>", methods=["GET"])
def get_ride_requests(ride_request_id):
    return service.get_ride_request_by_id(ride_request_id)


@app.route("/api/rides/v1", methods=["POST"])
def request_new_ride():
    data = request.json

    if not mandatory_new_ride_request_fields.issubset(data.keys()):
        return "Required fields are missing. Please include the fields in the payload. {}".format(
            mandatory_new_ride_request_fields)
    else:
        try:

            if 'vehicle_type' not in data.keys():
                selected_vehicle_type = Taxi_Type.ALL
            else:
                selected_vehicle_type = str(data['vehicle_type']).upper()

                if selected_vehicle_type == Taxi_Type.ECO.value:
                    selected_vehicle_type = Taxi_Type.ECO
                elif selected_vehicle_type == Taxi_Type.LUXURY.value:
                    selected_vehicle_type = Taxi_Type.LUXURY
                elif selected_vehicle_type == Taxi_Type.UTILITY.value:
                    selected_vehicle_type = Taxi_Type.UTILITY
                elif selected_vehicle_type == Taxi_Type.DELUXE.value:
                    selected_vehicle_type = Taxi_Type.DELUXE
                else:
                    selected_vehicle_type = Taxi_Type.ALL

            new_ride_request = RequestNewRideDTO(rider_id=data['rider_id'], vehicle_type=selected_vehicle_type,
                                                 start_latitude=data['start_latitude'],
                                                 start_longitude=data['start_longitude'],
                                                 destination_longitude=data['destination_longitude'],
                                                 destination_latitude=data['destination_latitude'])
            return service.request_ride(new_ride_request)  # return "Successfully requested the ride"
        except Exception as e:
            traceback.print_exc()
            return "Failed to request the ride. Error {}".format(e.__cause__)


@app.route("/api/rides/v1/<string:ride_request_id>/confirm_ride", methods=["POST"])
def confirm_ride(ride_request_id):
    data = request.json
    if not mandatory_confirm_ride_fields.issubset(data.keys()):
        return "Required fields are missing. Please include the fields in the payload. {}".format(
            mandatory_confirm_ride_fields)
    else:
        confirm_ride_dto = ConfirmRideDTO(taxi_id=data['taxi_id'], ride_request_id=ride_request_id,
                                          vehicle_type=Taxi_Type[str(data['vehicle_type']).upper()])
        return service.confirm_ride_request(confirm_ride_dto)


@app.route("/api/rides/v1/<string:ride_request_id>/start_trip", methods=["POST"])
def start_trip(ride_request_id):
    return service.start_trip(ride_request_id)


@app.route("/api/rides/v1/<string:ride_request_id>/complete_trip", methods=["POST"])
def complete_ride(ride_request_id):
    data = request.json
    return service.complete_ride_request(ride_request_id)


######## Trip Summmry endpoint
@app.route("/api/rides/v1/trips", methods=["GET"])
def get_all_trips():
    return Trip_Summary_Service.get_all_trips()


@app.route("/api/rides/v1/trips/<string:ride_request_id>", methods=["GET"])
def get_trip_by_ride_request_id(ride_request_id):
    return Trip_Summary_Service.get_trip_by_ride_request_id(ride_request_id)


# Run the service on the local server it has been deployed to,
# listening on port 8080.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
