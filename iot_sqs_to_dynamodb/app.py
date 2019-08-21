import json

import boto3

print('Loading function')

dynamo = boto3.client('dynamodb')


def lambda_handler(event, context):
    operations = {
        'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
        'POST': lambda dynamo, x: dynamo.put_item(**x),
        'PUT': lambda dynamo, x: dynamo.update_item(**x),
    }

    for record in event['Records']:
        payload = json.loads(record['body'])
        operation = record['messageAttributes']['Method']['stringValue']
        if operation in operations:
            operations[operation](dynamo, payload)
            return '{} successful'.format(operation)
        else:
            return 'Unsupported method \'{}\''.format(operation)
