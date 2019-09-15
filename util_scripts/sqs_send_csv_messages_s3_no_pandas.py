import datetime
import json
import logging
import os

import boto3
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

    iot_messages = obj['Body'].read().decode('utf-8').split()
    iot_messages.pop(0)
    for message in iot_messages:
        message = message.split(',')
        message = convert_and_send(message)
        message = json.dumps(message, separators=(',', ':'))
        print(message)
        response = send_sqs_message(message)
        if response is not None:
            logging.info(f'Sent SQS message ID: {response["MessageId"]}')


def convert_and_send(message):
    """
    Convert CSV file row to IoT message dictionary object.
    Drop millisecond precision from timestamp conversion.

    :param message: CSV file row containing an IoT message
    :return: Message dictionary object
    """
    converted_ts = datetime.datetime.fromtimestamp(float(message[0]))
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
                        'S': message[1]
                    },
                'source':
                    {
                        'S': message[2]
                    },
                'local_dest':
                    {
                        'S': message[3]
                    },
                'local_avg':
                    {
                        'N': message[4]
                    },
                'remote_dest':
                    {
                        'S': message[5]
                    },
                'remote_avg':
                    {
                        'N': message[6]
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
