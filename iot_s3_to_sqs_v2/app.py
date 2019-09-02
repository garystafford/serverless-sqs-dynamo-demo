import datetime
import json
import logging
import os
import urllib.parse

import boto3
from botocore.exceptions import ClientError

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(asctime)s: %(message)s'
)

logging.info('Loading function')

# Environment variables (set by SAM template)
sqs_queue_url = os.getenv("QUEUE_URL")
table_name = os.getenv("TABLE_NAME")

# AWS clients
sqs_client = boto3.client('sqs')
s3_client = boto3.client('s3')


def lambda_handler(event, context):
    logging.debug('Received event: ' + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        logging.debug('CONTENT TYPE: ' + response['ContentType'])
        if response['ContentType'] == 'text/csv':
            get_messages_csv(response)
        return 0
    except Exception as e:
        logging.error(e)
        logging.error('Error getting object {} from bucket {}. '
                      'Make sure they exist and your bucket is in the same region as this function.'
                      .format(key, bucket))
        raise e


def get_messages_csv(response):
    """
    Read CSV file containing IoT messages.

    :return:
    """
    iot_messages = response['Body'].read().decode('utf-8').split()
    iot_messages.pop(0)  # remove header row
    for row in iot_messages:
        message = row.split(',')
        message = convert_message(message)
        message = json.dumps(message, separators=(',', ':'))
        logging.debug(message)
        response = send_sqs_message(message)
        if response is not None:
            logging.info('Sent SQS message ID: ' + response['MessageId'])


def convert_message(message):
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
