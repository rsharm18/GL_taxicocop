import pymongo

from taxi_management_service.service.com.taxicoop.setup.Data_Generator import Data_Generator

db_client = pymongo.MongoClient(
    "mongodb+srv://taxicoop:admin123@cluster0.ykco3.mongodb.net/?retryWrites=true&w=majority")


class DB_Helper:

    # db = client.test

    @staticmethod
    def configure_db():
        db = db_client.test
        # Create a Database
        aggregator_db = db_client['taxi_management']
        # Create Collections
        taxis = aggregator_db['taxis']

        # if taxis:
        dummy_data = {
            'name': "Toofan",
            'type': "Luxury",
            'location': {
                'type': "Point",
                'coordinates': [28.65195, 77.23149]
            }
        }

        count = taxis.estimated_document_count()
        if count == 0:
            print("Adding dummy Data")
            data = Data_Generator.generate_taxi_data(50)
            taxis.insert_many(data)
