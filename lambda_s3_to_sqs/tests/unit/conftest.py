import os

import pytest

TABLE_NAME = os.getenv('TABLE_NAME')
S3_DATA_BUCKET = os.getenv('S3_DATA_BUCKET')

CVS_FILE_NAME = 'data_good_msg.csv'


@pytest.fixture(scope='module')
def messages():
    return [
        '978339661,location-03,wireless,router-1,1.11,device-1,8.88',
        '978339662,location-03,wireless,router-1,2.22,device-1,9.99'
    ]


@pytest.fixture(scope='module')
def message_string():
    return '978339663,location-03,wireless,router-1,3.33,device-1,7.77'


@pytest.fixture(scope='module')
def message_json():
    return "{\"TableName\":\"" + TABLE_NAME + "\",\"Item\":{\"date\": " + \
           "{\"S\": \"2001-01-01\"}, \"time\": {\"S\": \"01:01:04\"},\"location\": {\"S\": \"location-03\"}, " + \
           "\"source\": {\"S\":\"wireless\"}, \"local_dest\": {\"S\": \"router-1\"}, \"local_avg\": " + \
           "{\"N\": \"5.55\"}, \"remote_dest\": {\"S\": \"device-1\"}, \"remote_avg\": {\"N\": \"11.11\"}}}"


@pytest.fixture(scope='module')
def post_event():
    """ Generates S3 Event"""
    return {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "name": S3_DATA_BUCKET,
                    },
                    "object": {
                        "key": CVS_FILE_NAME,
                    }
                }
            }
        ]
    }
