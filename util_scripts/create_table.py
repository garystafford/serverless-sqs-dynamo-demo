import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# timestamp,location,source,local_dest,local_avg,remote_dest,remote_avg
# 1559040909.3853335,location-03,wireless,router-1,4.39,device-1,9.09

table_name = 'IotData'


def main():
    # Create the DynamoDB table.
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'timestamp',
                'KeyType': 'HASH' # Partition key
            },
            {
                'AttributeName': 'location',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'timestamp',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'location',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 2,
            'WriteCapacityUnits': 2
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)

    # Print out some data about the table.
    print(table.item_count)


if __name__ == '__main__':
    main()
