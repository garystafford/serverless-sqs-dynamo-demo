import datetime
import os

import pytest

AWS_REGION = os.getenv("AWS_REGION")
SQS_QUEUE_ARN = os.getenv("SQS_QUEUE_ARN")
TABLE_NAME = os.getenv("TABLE_NAME")

date_time = datetime.date


@pytest.fixture(scope="module")
def post_event():
    """ Generates SQS event containing POST"""
    post_body = "{\"TableName\":\"" + TABLE_NAME + "\",\"Item\":{\"date\": " + \
                "{\"S\": \"2001-01-01\"}, \"time\": {\"S\": \"01:01:07\"},\"location\": {\"S\": \"location-03\"}, " + \
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
                    "eventSourceARN": SQS_QUEUE_ARN,
                    "awsRegion": AWS_REGION
                }
            }
        ]
    }


@pytest.fixture(scope="module")
def put_event():
    """ Generates SQS event containing PUT"""
    put_body = "{\"TableName\": \"" + TABLE_NAME + "\", " + \
               "\"Key\": {\"date\": {\"S\": \"2001-01-01\"},\"time\": {\"S\": \"01:01:07\"}}, " + \
               "\"UpdateExpression\": \"set remote_avg = :val1\", " + \
               "\"ExpressionAttributeValues\": {\":val1\": {\"N\": \"9.00\"}}}"
    return {
        "Records": [
            {
                "body": put_body,
                "messageAttributes": {
                    "Method": {
                        "stringValue": "PUT",
                        "stringListValues": [],
                        "binaryListValues": [],
                        "dataType": "String"
                    },
                    "eventSource": "aws:sqs",
                    "eventSourceARN": SQS_QUEUE_ARN,
                    "awsRegion": AWS_REGION
                }
            }
        ]
    }


@pytest.fixture(scope="module")
def delete_event():
    """ Generates SQS event containing DELETE"""
    delete_body = "{\"TableName\": \"" + TABLE_NAME + "\", " + \
                  "\"Key\": {\"date\": {\"S\": \"2001-01-01\"}, \"time\": {\"S\": \"01:01:07\"}}}"
    return {
        "Records": [
            {
                "body": delete_body,
                "messageAttributes": {
                    "Method": {
                        "stringValue": "DELETE",
                        "stringListValues": [],
                        "binaryListValues": [],
                        "dataType": "String"
                    },
                    "eventSource": "aws:sqs",
                    "eventSourceARN": SQS_QUEUE_ARN,
                    "awsRegion": AWS_REGION
                }
            }
        ]
    }


@pytest.fixture(scope="module")
def get_event():
    """ Generates SQS event containing GET"""
    get_body = "{\"TableName\": \"" + TABLE_NAME + "\", " + \
               "\"Key\": {\"date\": {\"S\": \"2001-01-01\"}, \"time\": {\"S\": \"01:01:07\"}}}"
    return {
        "Records": [
            {
                "body": get_body,
                "messageAttributes": {
                    "Method": {
                        "stringValue": "GET",
                        "stringListValues": [],
                        "binaryListValues": [],
                        "dataType": "String"
                    },
                    "eventSource": "aws:sqs",
                    "eventSourceARN": SQS_QUEUE_ARN,
                    "awsRegion": AWS_REGION
                }
            }
        ]
    }


@pytest.fixture(scope="module")
def get_all_event():
    """ Generates SQS event containing GET_ALL (SCAN)"""
    get_all_body = "{\"TableName\": \"" + TABLE_NAME + "\"}"
    return {
        "Records": [
            {
                "body": get_all_body,
                "messageAttributes": {
                    "Method": {
                        "stringValue": "GET_ALL",
                        "stringListValues": [],
                        "binaryListValues": [],
                        "dataType": "String"
                    },
                    "eventSource": "aws:sqs",
                    "eventSourceARN": SQS_QUEUE_ARN,
                    "awsRegion": AWS_REGION
                }
            }
        ]
    }
