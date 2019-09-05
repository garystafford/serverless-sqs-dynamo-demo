import datetime
import os

import pytest

AWS_REGION = os.getenv("AWS_REGION")
SQS_QUEUE = os.getenv("SQS_QUEUE")
TABLE_NAME = os.getenv("TABLE_NAME")

date_time = datetime.date


@pytest.fixture(scope="module")
def messages():
    return 'timestamp,location,source,local_dest,local_avg,remote_dest,remote_avg\n' \
           '1559040909.3853335,lab-5,wireless,router-1,4.39,device-1,9.09\n' \
           '1559040919.5273902,lab-5,wireless,router-1,0.49,device-1,16.75'


@pytest.fixture(scope="module")
def message_string():
    return '1559040909.3853335,lab-5,wireless,router-1,4.39,device-1,9.09'


@pytest.fixture(scope="module")
def message_json():
    return "{\"TableName\":\"" + TABLE_NAME + "\",\"Item\":{\"date\": " + \
           "{\"S\": \"2000-01-01\"}, \"time\": {\"S\": \"06:45:43\"},\"location\": {\"S\": \"lab-5\"}, " + \
           "\"source\": {\"S\":\"wireless\"}, \"local_dest\": {\"S\": \"router-1\"}, \"local_avg\": " + \
           "{\"N\": \"5.32\"}, \"remote_dest\": {\"S\": \"device-1\"}, \"remote_avg\": {\"N\": \"11.01\"}}}"


@pytest.fixture(scope="module")
def apigw_event():
    """ Generates POST API GW Event"""
    post_body = "{\"TableName\":\"" + TABLE_NAME + "\",\"Item\":{\"date\": " + \
                "{\"S\": \"2000-01-01\"}, \"time\": {\"S\": \"06:45:43\"},\"location\": {\"S\": \"lab-5\"}, " + \
                "\"source\": {\"S\":\"wireless\"}, \"local_dest\": {\"S\": \"router-1\"}, \"local_avg\": " + \
                "{\"N\": \"5.32\"}, \"remote_dest\": {\"S\": \"device-1\"}, \"remote_avg\": {\"N\": \"11.01\"}}}"
    return {
        "Records": [
            {
                "body": post_body,
                "messageAttributes": {
                    "Method": {
                        "stringValue": "POST",
                        "stringListValues": [],
                        "binaryListValues": [],
                        "dataType": "String"
                    },
                    "eventSource": "aws:sqs",
                    "eventSourceARN": SQS_QUEUE,
                    "awsRegion": AWS_REGION
                }
            }
        ]
    }
