import random
from datetime import date, datetime
from time import sleep

import requests
from faker import Faker

fake = Faker(['en_IN', 'en-US', 'en_US', 'en_US', 'en-US'])

REGISTER_USER_URL = "http://taxicoop-api-load-balancer-898563336.us-east-1.elb.amazonaws.com/api/users/v1/register"

SIMULATED_USER_COUNT = 80


def generate_user_data() -> []:
    count = SIMULATED_USER_COUNT
    while count > 0:
        count -= 1
        first_name = fake.first_name()
        last_name = fake.last_name()
        new_user = {
            "name": f"{first_name} {last_name}",
            "email": f"{first_name}.{last_name}@{fake.domain_name()}",
            "contact_info": "xxxxx"
        }

        response = requests.post(REGISTER_USER_URL, json=new_user)
        sleep(0.5)
        print(response)


def generate_random_date() -> str:
    year = random.randint(2018, 2022)
    month = random.randint(1, 12)
    day = random.randint(1, 25)
    return date(year, month, day).isoformat()


if __name__ == "__main__":
    generate_user_data()
