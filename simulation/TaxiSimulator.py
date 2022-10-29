import random
from datetime import date
from time import sleep

import requests
from faker import Faker

from model.Taxi import RegisterNewTaxiDTO, Taxi_Type

fake = Faker(['en_IN', 'en-US', 'en_US', 'en_US', 'en-US'])

# taxi_status_list = list(Taxi_Status)
taxi_type_list = list(Taxi_Type)

starting_longitude = 88.358536
ending_longitude = 90.358536

starting_latitude = 22.578005
ending_latitude = 23.578005

REGISTER_TAXI_URL = "http://taxicoop-api-load-balancer-898563336.us-east-1.elb.amazonaws.com/api/taxi/v1/register"

SIMULATED_TAXI_COUNT = 80


def generate_taxi_data() -> []:
    count = SIMULATED_TAXI_COUNT
    while count > 0:
        count -= 1
        first_name = fake.first_name()
        last_name = fake.last_name()
        taxi_type: Taxi_Type = random.choice(taxi_type_list)
        new_taxi_dto = RegisterNewTaxiDTO(
            name=f"{first_name} {last_name}",
            email=f"{first_name}.{last_name}@{fake.domain_name()}",
            vehicle_type=taxi_type,
            license_plate=generate_license_plate(),
            latitude=round(random.uniform(starting_latitude, ending_latitude), 6),
            longitude=round(random.uniform(starting_longitude, ending_longitude), 6)
        ).__dict__

        response = requests.post(REGISTER_TAXI_URL, json=new_taxi_dto)
        sleep(0.5)
        print(response)


def generate_random_date() -> str:
    year = random.randint(2018, 2022)
    month = random.randint(1, 12)
    day = random.randint(1, 25)
    return date(year, month, day).isoformat()


def generate_license_plate():
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    nums = '0123456789'
    return ''.join([random.choice(chars) for i in range(3)] + [random.choice(nums) for i in range(4)])


if __name__ == "__main__":
    generate_taxi_data()
