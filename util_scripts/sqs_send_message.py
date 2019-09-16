import json
import logging
import os
import boto3
from botocore.exceptions import ClientError

sqs_client = boto3.client('sqs')

sqs_queue_url = os.getenv("SQS_QUEUE_URL")
table_name = os.getenv("TABLE_NAME")


def send_sqs_message(message):
    """
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
    """Exercise send_sqs_message()"""

    # Assign this value before running the program

    # Set up logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s: %(asctime)s: %(message)s')

    # timestamp,location,source,local_dest,local_avg,remote_dest,remote_avg
    # 1559040909.3853335,location-03,wireless,router-1,4.39,device-1,9.09

    message = {
        'TableName': table_name,
        'Item':
            {
                'date':
                    {
                        'S': '2000-01-01'
                    },
                'time':
                    {
                        'S': '06:45:43.128341'
                    },
                'location':
                    {
                        'S': 'location-03'
                    },
                'source':
                    {
                        'S': 'wireless'
                    },
                'local_dest':
                    {
                        'S': 'router-1'
                    },
                'local_avg':
                    {
                        'N': '5.32'
                    },
                'remote_dest':
                    {
                        'S': 'device-1'
                    },
                'remote_avg':
                    {
                        'N': '11.01'
                    }
            }
    }

    print(str(message))

    message = json.dumps(message, separators=(',', ':'))
    print(message)

    messages = [
        message
    ]

    # Send SQS messages
    for message in messages:
        msg = send_sqs_message(message)
        if msg is not None:
            logging.info(f'Sent SQS message ID: {msg["MessageId"]}')


if __name__ == '__main__':
    main()
