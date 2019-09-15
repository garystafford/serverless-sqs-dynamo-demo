import datetime
import json
import logging
import os

import boto3
import pandas as pd
from botocore.exceptions import ClientError

# Environment variables
s3_bucket_path = os.getenv("S3_BUCKET")
sqs_queue_url = os.getenv("SQS_QUEUE_URL")
table_name = os.getenv("TABLE_NAME")
object_path = 'iot_data.csv'

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(asctime)s: %(message)s'
)

# AWS clients
sqs_client = boto3.client('sqs')
s3_client = boto3.client('s3')


def get_messages_csv():
    """
    Read CSV file containing IoT messages.

    :return:
    """
    obj = s3_client.get_object(
        Bucket=s3_bucket_path,
        Key=object_path
    )

    iot_messages = pd.read_csv(obj['Body'])
    for index, row in iot_messages.iterrows():
        message = convert_and_send(row)
        message = json.dumps(message, separators=(',', ':'))
        response = send_sqs_message(message)
        if response is not None:
            logging.info(f'Sent SQS message ID: {response["MessageId"]}')

        # send_sqs_message(message)


def convert_and_send(row):
    """
    Convert CSV file row to IoT message dictionary object.
    Drop millisecond precision from timestamp conversion.

    :param row: CSV file row containing an IoT message
    :return: Message dictionary object
    """
    converted_ts = datetime.datetime.fromtimestamp(float(row['timestamp']))
    message = {
        'TableName': table_name,
        'Item':
            {
                'date':
                    {
                        'S': str(converted_ts.date())
                    },
                'time':
                    {
                        'S': str(converted_ts.time().strftime('%H:%M:%S'))
                    },
                'location':
                    {
                        'S': row['location']
                    },
                'source':
                    {
                        'S': row['source']
                    },
                'local_dest':
                    {
                        'S': row['local_dest']
                    },
                'local_avg':
                    {
                        'N': row['local_avg']
                    },
                'remote_dest':
                    {
                        'S': row['remote_dest']
                    },
                'remote_avg':
                    {
                        'N': row['remote_avg']
                    }
            }
    }
    return message


def send_sqs_message(message):
    """
    Send JSON-format IoT message to SQS.

    :param message: String message body
    :return: Dictionary containing information about the sent message. If
        error, returns None.
    """

    # Send the SQS message
    try:
        msg = sqs_client.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody=message,
            DelaySeconds=0,
            MessageAttributes={
                'Method': {
                    'StringValue': 'POST',
                    'DataType': 'String'
                }
            }
        )
    except ClientError as e:
        logging.error(e)
        return None
    return msg


def main():
    get_messages_csv()


if __name__ == '__main__':
    main()
