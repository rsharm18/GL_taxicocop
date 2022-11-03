import json

import requests

TAXI_BASE_URL = "http://taxicoop-api-load-balancer-898563336.us-east-1.elb.amazonaws.com/api/taxi/v1"
def lambda_handler(event, context):

    try:
        print(" payload received : {}".format(event))
        url = '{}/{}/book'.format(TAXI_BASE_URL, event['taxi_id'])
        response = requests.post(url, json=event)
        print(response)

        return {
            'statusCode': 200,
            'body': json.dumps('{} Ride book request sent successfully'.format(event))
        }
    except Exception as ex:
        print(ex)
        print("Error Occurred. Please check logs ")

    return {
        'statusCode': 400,
        'body': json.dumps('Error Processing {} for baseURL {}'.format(event, TAXI_BASE_URL))
    }
