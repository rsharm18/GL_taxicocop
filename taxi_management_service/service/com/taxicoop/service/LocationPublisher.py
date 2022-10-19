import random

from taxi_management_service.service.com.taxicoop.model.Location import Location
from taxi_management_service.service.com.taxicoop.service.DBHelper import DB_Helper


class LocationPublisher:

    @staticmethod
    def publish_location():
        taxis = DB_Helper.get_all_taxis()
        for taxi in taxis:
            loc = taxi['location']
            coordinates = loc['coordinates']
            longitude = float(coordinates[0])
            latitiude = float(coordinates[1])

            longitude = round(random.uniform(latitiude, latitiude + random.randint(1, 4)), 2)
            latitiude = round(random.uniform(latitiude, latitiude + random.randint(1, 10)), 2)

            final_location = Location(entity_id=taxi['taxi_id'],
                                      status=taxi['status'],
                                      entity_type='Taxi',
                                      latitude=latitiude,
                                      longitude=longitude,
                                      vehicle_type=taxi['type']
                                      )
            DB_Helper.publish_taxi_location(final_location)
            print(" longitude= {}, latitiude={}".format(longitude, latitiude))
