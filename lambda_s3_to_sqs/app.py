import boto3
import datetime
import json
import logging
import os
import urllib.parse
from botocore.exceptions import ClientError

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logger.info('Loading function')

# Environment variables (set by SAM template)
sqs_queue_url = os.getenv("SQS_QUEUE_URL")
table_name = os.getenv("TABLE_NAME")

# AWS clients
sqs_client = boto3.client('sqs')
s3_client = boto3.client('s3')


def lambda_handler(event, context):
    logger.debug('Received event: {}'.format(event))

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'],
        encoding='utf-8'
    )
    messages = read_csv_file(bucket, key)
    process_messages(messages)
    return 0


def read_csv_file(bucket, key):
    """
    Read messages from CSV file.

    :param bucket: S3 Bucket Name
    :param key: CSV file name
    :return: messages
    """
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        logger.debug('CONTENT TYPE: {}'.format(response['ContentType']))
        if response['ContentType'] == 'text/csv':
            messages = response['Body'].read().decode('utf-8').split()
            messages.pop(0)  # remove header row
            return messages
    except Exception as e:
        logger.error(e)
        logger.error('Error getting object {} from bucket {}. '
                     'Make sure they exist and your bucket is in the same region as this function.'
                     .format(key, bucket))
        raise e


def process_messages(messages):
    """
    Process messages.

    :param messages: Messages from CSV file
    :return: 0 or -1
    """
    try:
        for row in messages:
            message = row.split(',')
            message = convert_message(message)
            message = json.dumps(message, separators=(',', ':'))
            logger.debug(message)
            response = send_sqs_message(message)
            if response is not None:
                logger.info('Sent SQS message ID: {}'.format(response['MessageId']))
        return 0
    except Exception as e:
        logger.error(e)
        return -1


def convert_message(message):
    """
    Convert CSV file row to message dictionary object.
    Drop millisecond precision from timestamp conversion.

    :param message: CSV file row containing a message
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
    Send JSON-format message to SQS.

    :param message: Dictionary message object
    :return: Dictionary containing information about the sent message. If
        error, returns None.
    """

    try:
        response = sqs_client.send_message(
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
        return response
    except ClientError as e:
        logger.error(e)
        return None
