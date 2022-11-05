import traceback
from datetime import datetime

from com.taxicoop.service.DBHelper import DB_Helper

def user_db_data_json(user_db_data):

    if user_db_data is None:
        return None

    return {
                'name': user_db_data['name'],
                'email': user_db_data['email'],
                'contact_info': user_db_data['contact_info'],
                'status': user_db_data['status'],
                'member_since': user_db_data['member_since']
            }

class UserService:

    # Since name should be unique in users collection, this provides a way to
    # fetch the user document based on the Email

    def find_by_email(self, email):
        key = {'email': email}
        return user_db_data_json(DB_Helper.get_single_data(key))

    # This first checks if a user already exists with that name. If it does, it populates latest_error and returns -1
    # If a user doesn't already exist, it'll insert a new document and return the same to the caller
    def insert_user(self, name, email, contact_info):

        user_document = self.find_by_email(email)
        if user_document:
            print("User already exists")
            raise ("User with email= {} already exists".format(email))

        user_data = {'name': name, 'email': email, 'contact_info': contact_info, 'status': 'AVAILABLE',
                     'member_since': datetime.now().isoformat()}
        return DB_Helper.insert_single_data(user_data)

    def get_all_Users(self):
        users = DB_Helper.get_all_user()
        result = []
        for user in users:
            result.append(user_db_data_json(user))
        return result

    def update_user(self, payload):
        try:
            DB_Helper.update_user(payload['email'], payload)
            return {
                'status': 'success',
                'message': 'Successfully updated the user data'
            }
        except Exception as ex:
            traceback.print_exc()

        return {
            'status': 'failed',
            'message': 'Error updating the user data'
        }
