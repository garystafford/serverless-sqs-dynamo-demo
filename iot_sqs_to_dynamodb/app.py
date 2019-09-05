import logging
from json import loads

import boto3

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Loading function')

dynamo_client = boto3.client('dynamodb')


def lambda_handler(event, context):
    operations = {
        'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
        'POST': lambda dynamo, x: dynamo.put_item(**x),
        'PUT': lambda dynamo, x: dynamo.update_item(**x),
        'GET': lambda dynamo, x: dynamo.get_item(**x),
        'GET_ALL': lambda dynamo, x: dynamo.scan(**x),
    }

    for record in event['Records']:
        payload = loads(record['body'], parse_float=str)
        operation = record['messageAttributes']['Method']['stringValue']
        if operation in operations:
            try:
                operations[operation](dynamo_client, payload)
                logger.info('{} successful'.format(operation))
                return 0
            except Exception as e:
                logger.error(e)
                return -1
        else:
            logger.error('Unsupported method \'{}\''.format(operation))
            return -1
