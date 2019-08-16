import boto3

# url example: https://queue.amazonaws.com/931066906971/QueueIotData

# Create SQS client
sqs = boto3.client('sqs')

queue_name = 'QueueIotData'


def main():
    # Create a SQS queue
    response = sqs.create_queue(
        QueueName=queue_name,
        Attributes={
            'DelaySeconds': '0',
            'MessageRetentionPeriod': '86400'
        }
    )

    print(response['QueueUrl'])


if __name__ == '__main__':
    main()
