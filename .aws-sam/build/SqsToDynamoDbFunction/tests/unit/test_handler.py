import pytest
import datetime

from ... import app

date_time = datetime.date


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""
    return {
        "Records": [
            {
                "body": "{\"TableName\":\"iot-dynamodb-IotDemoTable-1N4QFAHEDD96E\",\"Item\":{\"date\":"
                        "{\"S\":\"2000-01-01\"},\"time\":{\"S\":\"06:45:43.128341\"},\"location\":{\"S\":\"lab-5\"},"
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
                    "eventSourceARN": "arn:aws:sqs:us-east-1:931066906971:iot-dynamodb-IotDemoQueue-PBICA74HO9GA",
                    "awsRegion": "us-east-1"
                }
            }
        ]
    }


def test_lambda_handler(apigw_event):
    ret = app.lambda_handler(apigw_event, '')
    assert ret.find('successful') != -1
