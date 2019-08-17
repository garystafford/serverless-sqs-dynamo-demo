from sys import path

import pytest

path.append('..')

import app


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "Records": [
            {
                "body": "{\"TableName\":\"iot-dynamodb-IotDemoTable-1E1VFYADYIPIL\",\"Item\":{\"date\":"
                        "{\"S\":\"2019-05-31\"},\"time\":{\"S\":\"06:45:43.128341\"},\"location\":{\"S\":\"lab-5\"},"
                        "\"source\":{\"S\":\"wireless\"},\"local_dest\":{\"S\":\"router-1\"},\"local_avg\":"
                        "{\"N\":\"5.32\"},\"remote_dest\":{\"S\":\"device-1\"},\"remote_avg\":{\"N\":\"11.01\"}}}",
                "messageAttributes": {
                    "Method": {
                        "stringValue": "POST",
                        "stringListValues": [],
                        "binaryListValues": [],
                        "dataType": "String"
                    },
                    "eventSource": "aws:sqs",
                    "eventSourceARN": "arn:aws:sqs:us-east-1:931066906971:iot-dynamodb-IotDemoQueue-XYWKCFK3DC6C",
                    "awsRegion": "us-east-1"
                }
            }
        ]
    }


def test_lambda_handler(apigw_event, mocker):
    ret = app.lambda_handler(apigw_event, '')
    assert ret.find('successful') != -1
