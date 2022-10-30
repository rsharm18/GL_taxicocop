import random
import uuid
from datetime import date


from faker import Faker

fake = Faker(['en_IN', 'en-US', 'en_US', 'en_US', 'en-US'])

class Data_Generator:

    @staticmethod
    def generate_user_data(count=50) -> []:
        user_list = []
        while count > 0:
            count -= 1
            first_name = fake.first_name()
            last_name = fake.last_name()

            user_list.append(User(user_id=str(uuid.uuid4()),
                                  user_name=f"{first_name} {last_name}",
                                  user_email=f"{first_name}.{last_name}@{fake.domain_name()}",

                                  user_mobile=Data_Generator.generate_mobilenumb(),
                                  ).__dict__)

        return user_list



    @staticmethod
    def generate_mobilenumb():
        chars = '91'
        nums = '0123456789'
        return ''.join([chars + [random.choice(nums) for i in range(10)]])
