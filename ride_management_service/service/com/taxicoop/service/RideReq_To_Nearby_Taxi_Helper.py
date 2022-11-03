import json
import traceback

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

from com.taxicoop.model.Ride_Request import Ride_Request

TOPIC = 'iot/topic/ride_request_confirmation_nearby_taxis'

clientId = 'RIDE_REQUEST_PUBLISHER'
ENDPOINT = "a6bhiotawus4w-ats.iot.us-east-1.amazonaws.com"
PORT = 8883

rootCAPath = 'com/taxicoop/certs/ride_request/AmazonRootCA1.pem'
privateKeyPath = 'com/taxicoop/certs/ride_request/ef6d8847efe38f98e53cf13555cf212332271d7198978300ea9e06bc5cedba68-private.pem.key'
certificatePath = 'com/taxicoop/certs/ride_request/ef6d8847efe38f98e53cf13555cf212332271d7198978300ea9e06bc5cedba68-certificate.pem.crt'
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


def send_ride_request_to_nearby_taxis(ride_request: Ride_Request):

    print(" ********** send_ride_request_to_nearby_taxis ********** \n\n")
    near_by_taxis = ride_request.near_by_taxis

    print(" near_by_taxis {}".format(near_by_taxis))

    for taxi in near_by_taxis:
        payload = {
            'taxi_id': taxi['taxi_id'],
            'start_location': ride_request.start_location,
            'destination_location': ride_request.destination_location,
            'ride_request_id': ride_request.ride_request_id
        }
        try:
            myAWSIoTMQTTClient.publish(TOPIC, json.dumps(payload), 1)
        except Exception as ex:
            traceback.print_exc()
