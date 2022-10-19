import random
import uuid
from datetime import date

from faker import Faker

from taxi_management_service.service.com.taxicoop.model.Taxi import Taxi, Taxi_Status, Taxi_Type

fake = Faker(['en_IN', 'en-US', 'en_US', 'en_US', 'en-US'])

# taxi_status_list = list(Taxi_Status)
taxi_type_list = list(Taxi_Type)


class Data_Generator:

    @staticmethod
    def generate_taxi_data(count=50) -> []:
        taxi_list = []
        while count > 0:
            count -= 1
            first_name = fake.first_name()
            last_name = fake.last_name()
            # taxi_status: Taxi_Status = random.choice(taxi_status_list)
            taxi_type: Taxi_Type = random.choice(taxi_type_list)

            taxi_list.append(Taxi(taxi_id=str(uuid.uuid4()),
                                  user_name=f"{first_name} {last_name}",
                                  status=Taxi_Status.AVAILABLE,
                                  type=taxi_type,
                                  owner_email=f"{first_name}.{last_name}@{fake.domain_name()}",
                                  member_since=Data_Generator.generate_random_date(),
                                  license_plate=Data_Generator.generate_license_plate()
                                  ).__dict__)

        return taxi_list

    @staticmethod
    def generate_random_date() -> str:
        year = random.randint(2018, 2022)
        month = random.randint(1, 12)
        day = random.randint(1, 25)
        return date(year, month, day).isoformat()

    @staticmethod
    def generate_license_plate():
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        nums = '0123456789'
        return ''.join([random.choice(chars) for i in range(3)] + [random.choice(nums) for i in range(4)])
