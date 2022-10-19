import traceback

from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler
from flask_cors import CORS

from com.taxicoop.service.taxi_service import Taxi_Service
from taxi_management_service.service.com.taxicoop.dto.RegisterNewTaxiDTO import RegisterNewTaxiDto
from taxi_management_service.service.com.taxicoop.model.Taxi import Taxi_Type
from taxi_management_service.service.com.taxicoop.service.DBHelper import DB_Helper
from taxi_management_service.service.com.taxicoop.service.LocationPublisher import LocationPublisher

app = Flask(__name__)
CORS(app)

service = Taxi_Service()

mandatory_new_taxi_fields = {'name', 'email', 'vehicle_type', 'license_plate', 'longitude', 'latitude'}


# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True


# initialize scheduler
scheduler = APScheduler()
# if you don't wanna use a config, you can set options here:
# scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()


# interval example
@scheduler.task('interval', id='publish_location', seconds=10, misfire_grace_time=900)
def job1():
    LocationPublisher.publish_location()


@app.route("/api/taxi/register", methods=["POST"])
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

            new_taxi = RegisterNewTaxiDto(name=data['name'], email=data['email'],
                                          vehicle_type=selected_vehicle_type,
                                          license_plate=data['license_plate'],
                                          latitude=data['latitude'],
                                          longitude=data['longitude'])
            service.register_taxi(new_taxi)
            return "Successfully registered the taxi"
        except Exception as e:
            traceback.print_exc()
            return "Failed to register taxi. Error {}".format(e.__cause__)


@app.route("/api/taxi/<string:taxi_id>/location", methods=["POST"])
def store_taxi_location(taxi_id):
    return jsonify(service.capture_location(taxi_id))


# Run the service on the local server it has been deployed to,
# listening on port 8080.
if __name__ == "__main__":
    DB_Helper.configure_db()
    app.run(host="0.0.0.0", port=8080, debug=True)
