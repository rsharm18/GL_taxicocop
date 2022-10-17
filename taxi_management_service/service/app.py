from flask import Flask, jsonify, json, Response, request
from flask_cors import CORS

from com.taxicoop.service.taxi_service import Taxi_Service

app = Flask(__name__)
CORS(app)

service = Taxi_Service()


@app.route("/api/taxi/register", methods=["POST"])
def register_taxi():
    return jsonify(service.register_taxi())


@app.route("/api/taxi/<string:taxi_id>/location", methods=["POST"])
def store_taxi_location(taxi_id):
    return jsonify(service.capture_location(taxi_id))


# Run the service on the local server it has been deployed to,
# listening on port 8080.
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
