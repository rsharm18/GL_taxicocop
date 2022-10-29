import random
from time import sleep

import requests
from faker import Faker

from model.RequestNewRideDTO import RequestNewRideDTO
from model.Taxi import Taxi_Type

fake = Faker(['en_IN', 'en-US', 'en_US', 'en_US', 'en-US'])

# taxi_status_list = list(Taxi_Status)
taxi_type_list = list(Taxi_Type)

starting_longitude = 88.358536
ending_longitude = 90.358536

starting_latitude = 22.578005
ending_latitude = 23.578005

TAXI_BASE_URL = "http://taxicoop-api-load-balancer-898563336.us-east-1.elb.amazonaws.com/api/taxi/v1"
RIDE_REQUEST_URL = "http://taxicoop-api-load-balancer-898563336.us-east-1.elb.amazonaws.com/api/rides/v1"

max_user_per_taxi = 8


def generate_ride_request_data():
    taxis = requests.get(TAXI_BASE_URL).json()

    for taxi in taxis:
        loc = taxi['location']
        coordinates = loc['coordinates']
        longitude = float(coordinates[0])
        latitude = float(coordinates[1])

        count = 0
        while count < 8:
            count += 1
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name}.{last_name}@{fake.domain_name()}"

            start_longitude = round(random.uniform(longitude, longitude + random.uniform(0.299999, 0.799999)), 6)
            start_latitude = round(random.uniform(latitude, latitude + random.uniform(0.299999, 0.799999)), 6)

            destination_longitude = round(random.uniform(longitude, longitude + random.uniform(0.899999, 0.999999)), 6)
            destination_latitude = round(random.uniform(latitude, latitude + random.uniform(0.899999, 0.999999)), 6)
            vehicle_type = taxi['type']

            request_ride = RequestNewRideDTO(rider_id=email, vehicle_type=vehicle_type,
                                             start_latitude=start_latitude,
                                             start_longitude=start_longitude,
                                             destination_longitude=destination_longitude,
                                             destination_latitude=destination_latitude).__dict__

            response = requests.post(RIDE_REQUEST_URL, json=request_ride)
            print(response)
            sleep(0.001)


if __name__ == "__main__":
    generate_ride_request_data()
