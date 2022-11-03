from datetime import datetime

from service.com.taxicoop.service import DBHelper


class UserService:


    # Since username should be unique in users collection, this provides a way to
    # fetch the user document based on the Email
    def find_by_username(self, username):
        key = {'username': username}
        return DBHelper.get_single_data(key)




    # This first checks if a user already exists with that username. If it does, it populates latest_error and returns -1
    # If a user doesn't already exist, it'll insert a new document and return the same to the caller
    def insert_user(self, username, email, contact_info):

        user_document = self.find_by_username(email)
        if (user_document):
        return -1
        user_data = {'username': username, 'email': email, 'contact_info': contact_info, 'status' : 'AVAILABLE', 'member_since' : datetime.now().isoformat() }
        return DBHelper.insert_single_data(user_data)


    def get_all_Users(self):
        users = DBHelper.get_all_user()
        result = []
        for user in users:
            name = user['username']
            email = user['email']
            contact_info = user['contact_info']
            status = user ['status']
            member_since = user['member_since']
            result.append(name=name, email=email, contact_info= contact_info , status = status, member_since= member_since).__dict__
        return result

