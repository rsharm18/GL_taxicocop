import random
import json
import datetime
import threading

import requests

from LocationPublisherHandler import publish_taxi_location_data

TAXI_BASE_URL = "http://taxicoop-api-load-balancer-898563336.us-east-1.elb.amazonaws.com/api/taxi/v1"


# location publisher
def initiate_publish():
    minute = None
    while True:
        # publish location data every minute
        if datetime.datetime.now().minute != minute:
            minute = datetime.datetime.now().minute
            threading.Thread(target=publish_taxi_location_data()).start()


# code for aws lambda function
def lambda_handler(event, context):
    try:
        print(" payload received : {}".format(event))
        url = '{}/{}/location'.format(TAXI_BASE_URL, event['entity_id'])
        response = requests.post(url, json=event)
        print(response)

        return {
            'statusCode': 200,
            'body': json.dumps('{} location data added successfully'.format(event))
        }
    except Exception as ex:
        print(ex)
        print("Error Occurred. Please check logs ")

    return {
        'statusCode': 400,
        'body': json.dumps('Error Processing {} for baseURL {}'.format(event, TAXI_BASE_URL))
    }


if __name__ == "__main__":
    initiate_publish()
