import traceback

from flask import Flask, request
from flask_cors import CORS

from com.taxicoop.dto.RequestNewRideDTO import RequestNewRideDTO
from com.taxicoop.model.Ride_Request import Taxi_Type
from com.taxicoop.service.Ride_Mgmt_Service import Ride_Service

app = Flask(__name__)
CORS(app)

service = Ride_Service()

mandatory_new_ride_request_fields = {'rider_id', 'longitude', 'latitude'}


@app.route("/api/ride/v1", methods=["POST"])
def request_new_ride():
    data = request.json

    if not mandatory_new_ride_request_fields.issubset(data.keys()):
        return "Required fields are missing. Please include the fields in the payload. {}".format(
            mandatory_new_ride_request_fields)
    else:
        try:

            if 'vehicle_type' not in data.keys():
                selected_vehicle_type = Taxi_Type.DELUXE
            else:
                selected_vehicle_type = str(data['vehicle_type']).upper()

                if selected_vehicle_type == Taxi_Type.ECO.value:
                    selected_vehicle_type = Taxi_Type.ECO
                elif selected_vehicle_type == Taxi_Type.LUXURY.value:
                    selected_vehicle_type = Taxi_Type.LUXURY
                elif selected_vehicle_type == Taxi_Type.UTILITY.value:
                    selected_vehicle_type = Taxi_Type.UTILITY
                else:
                    selected_vehicle_type = Taxi_Type.DELUXE

            new_ride_request = RequestNewRideDTO(rider_id=data['rider_id'], vehicle_type=selected_vehicle_type,
                                                 latitude=data['latitude'],
                                                 longitude=data['longitude'])
            service.request_ride(new_ride_request)
            return "Successfully requested the ride"
        except Exception as e:
            traceback.print_exc()
            return "Failed to request the ride. Error {}".format(e.__cause__)


# Run the service on the local server it has been deployed to,
# listening on port 8080.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
