import pymongo

db_conn = pymongo.MongoClient(
    "mongodb+srv://taxicoop:admin123@cluster0.ykco3.mongodb.net/?retryWrites=true&w=majority")

db = db_conn["user_management"]
user_mgmt = db['users']


class DB_Helper:

    # This method finds a single document using field information provided in the key parameter
    # It assumes that the key returns a unique document. It returns None if no document is found
    @staticmethod
    def get_single_data(key):
        return user_mgmt.find_one(key)

    # This method inserts the data in a new document. It assumes that any uniqueness check is done by the caller
    @staticmethod
    def insert_single_data(data):
        document = user_mgmt.insert_one(data)
        return document.inserted_id

    @staticmethod
    def get_all_user():
        return user_mgmt.find()

    @staticmethod
    def update_user(email, values):
        query = {"email": email}
        update = {"$set": values}
        user_data = user_mgmt.find_one(query)
        if user_data is None:
            raise Exception("Invalid User email id")

        user_mgmt.update_one(query, update)
