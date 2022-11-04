import json
import random
import threading
import traceback
from datetime import datetime
from time import sleep

import requests
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

TAXI_BASE_URL = "http://taxicoop-api-load-balancer-898563336.us-east-1.elb.amazonaws.com/api/taxis/v1"
TOPIC = 'iot/topic/location'

clientId = 'TAXI_LOCATION_PUBLISHER'
ENDPOINT = "a6bhiotawus4w-ats.iot.us-east-1.amazonaws.com"
PORT = 8883
rootCAPath = 'certs/AmazonRootCA1.pem'
privateKeyPath = 'certs/1a633a4ddef7e29ea9dda5129aff3c14b743df31084e359d1925e957acb0558e-private.pem.key'
certificatePath = 'certs/1a633a4ddef7e29ea9dda5129aff3c14b743df31084e359d1925e957acb0558e-certificate.pem.crt'
# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, PORT)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()


def initiate_publish():
    minute = None
    while True:
        # publish location data every minute
        if datetime.now().minute != minute:
            minute = datetime.now().minute
            threading.Thread(target=publish_taxi_location_data()).start()


def publish_taxi_location_data():
    print("publish_taxi_location_data called")
    taxis = requests.get(TAXI_BASE_URL).json()
    for taxi in taxis:
        loc = taxi['location']
        coordinates = loc['coordinates']
        longitude = float(coordinates[0])
        latitude = float(coordinates[1])

        longitude = round(random.uniform(longitude, longitude + random.uniform(0.899999, 0.999999)), 6)
        latitude = round(random.uniform(latitude, latitude + random.uniform(0.899999, 0.999999)), 6)

        payload = {
            "entity_id": taxi['taxi_id'],
            "status": taxi['status'],
            "entity_type": 'Taxi',
            "latitude": latitude,
            "longitude": longitude,
            "vehicle_type": taxi['type']
        }
        try:
            myAWSIoTMQTTClient.publish(TOPIC, json.dumps(payload), 1)
            sleep(0.01)
        except Exception as ex:
            traceback.print_exc()

    print("publish_taxi_location_data completed")


if __name__ == "__main__":
    initiate_publish()
