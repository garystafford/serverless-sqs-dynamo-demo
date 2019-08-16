import json

import boto3

print('Loading function...')
dynamo = boto3.client('dynamodb')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        }
    }


def lambda_handler(event, context):
    operations = {
        'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
        'POST': lambda dynamo, x: dynamo.put_item(**x),
        'PUT': lambda dynamo, x: dynamo.update_item(**x),
    }

    for record in event['Records']:
        print('Event:', event)
        print('Context:', context)
        payload = json.loads(record['body'])
        operation = record['messageAttributes']['Method']['stringValue']
        print('Payload:', payload)
        print('Method Attribute:', operation)
        if operation in operations:
            respond(None, operations[operation](dynamo, payload))
        else:
            respond(ValueError('Unsupported method "{}"'.format(operation)))
