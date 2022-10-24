import traceback

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
from flask_cors import CORS

from com.taxicoop.dto.RegisterNewLocationDTO import RegisterNewLocationDTO
from com.taxicoop.dto.RegisterNewTaxiDTO import RegisterNewTaxiDTO
from com.taxicoop.model.Taxi import Taxi_Type
from com.taxicoop.service.DBHelper import DB_Helper
from com.taxicoop.service.LocationJobHandler import LocationJobHandler
from com.taxicoop.service.taxi_service import Taxi_Service

app = Flask(__name__)
CORS(app)

service = Taxi_Service()

mandatory_new_taxi_fields = {'name', 'email', 'vehicle_type', 'license_plate', 'longitude', 'latitude'}
mandatory_new_location_fields = {'entity_type', 'vehicle_type', 'status', 'longitude', 'latitude'}
mandatory_nearby_taxi_location_fields = {'longitude', 'latitude'}

scheduler = BackgroundScheduler()
# scheduler.add_job(LocationPublisher.publish_location, "interval", seconds=45, misfire_grace_time=40, jitter=10,
#                   max_instances=1, id="publish_location", name="publish_location")
scheduler.add_job(LocationJobHandler.delete_stale_data, "interval", seconds=120, misfire_grace_time=60, jitter=30,
                  max_instances=1, id="delete_stale_locations", name="delete_stale_locations")
scheduler.start()


## add a new taxi
@app.route("/api/taxi/v1", methods=["GET"])
def get_all_taxis():
    return service.get_all_taxis()

## add a new taxi
@app.route("/api/taxi/v1/register", methods=["POST"])
def register_taxi():
    data = request.json

    if not mandatory_new_taxi_fields.issubset(data.keys()):
        return "Required fields are missing. Please include the fields in the payload. {}".format(
            mandatory_new_taxi_fields)
    else:
        try:
            selected_vehicle_type = str(data['vehicle_type']).upper()

            if selected_vehicle_type == Taxi_Type.ECO.value:
                selected_vehicle_type = Taxi_Type.ECO
            elif selected_vehicle_type == Taxi_Type.LUXURY.value:
                selected_vehicle_type = Taxi_Type.LUXURY
            elif selected_vehicle_type == Taxi_Type.UTILITY.value:
                selected_vehicle_type = Taxi_Type.UTILITY
            else:
                selected_vehicle_type = Taxi_Type.DELUXE

            new_taxi = RegisterNewTaxiDTO(name=data['name'], email=data['email'], vehicle_type=selected_vehicle_type,
                                          license_plate=data['license_plate'], latitude=data['latitude'],
                                          longitude=data['longitude'])
            service.register_taxi(new_taxi)
            return "Successfully registered the taxi"
        except Exception as e:
            traceback.print_exc()
            return "Failed to register taxi. Error {}".format(e.__cause__)


## add a taxi's location
@app.route("/api/taxi/v1/<string:taxi_id>/location", methods=["POST"])
def store_taxi_location(taxi_id):
    data = request.json
    if not mandatory_new_location_fields.issubset(data.keys()):
        return "Required fields are missing. Please include the fields in the payload. {}".format(
            mandatory_new_location_fields)
    else:
        try:
            new_location = RegisterNewLocationDTO(entity_id=taxi_id, entity_type=data['entity_type'],
                                                  vehicle_type=str(data['vehicle_type']).upper(),
                                                  longitude=data['longitude'], latitude=data['latitude'],
                                                  status=str(data['status']).upper())
            service.capture_location(new_location)
            return "Successfully registered the location"
        except Exception as e:
            traceback.print_exc()
            return "Failed to register location. Error {}".format(e.__cause__)


## get nearby taxis
@app.route("/api/taxi/v1/nearby-taxis", methods=["POST"])
def get_available_rides():
    data = request.json

    if not mandatory_nearby_taxi_location_fields.issubset(data.keys()):
        return "Required fields are missing. Please include the fields in the payload. {}".format(
            mandatory_nearby_taxi_location_fields)
    else:

        selected_vehicle_type = Taxi_Type.ALL
        if 'vehicle_type' in data.keys():
            if data['vehicle_type'] == Taxi_Type.ECO.value:
                selected_vehicle_type = Taxi_Type.ECO
            elif data['vehicle_type'] == Taxi_Type.LUXURY.value:
                selected_vehicle_type = Taxi_Type.LUXURY
            elif data['vehicle_type'] == Taxi_Type.UTILITY.value:
                selected_vehicle_type = Taxi_Type.UTILITY
            elif data['vehicle_type'] == Taxi_Type.DELUXE.value:
                selected_vehicle_type = Taxi_Type.DELUXE
            else:
                selected_vehicle_type = Taxi_Type.ALL

        return service.get_nearby_taxis(user_latitude=data['latitude'],
                                        user_longitude=data['longitude'],
                                        vehicle_type=selected_vehicle_type)

@app.route("/api/taxi/v1/<string:taxi_id>/book", methods=["POST"])
def confirm_ride(taxi_id):
    return service.reserve(taxi_id)

# Run the service on the local server it has been deployed to,
# listening on port 8080.
if __name__ == "__main__":
    DB_Helper.configure_db()
    app.run(host="0.0.0.0", port=8080, debug=True)
