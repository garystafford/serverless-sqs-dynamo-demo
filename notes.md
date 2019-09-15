```bash
# initiate
sam init --runtime nodejs10.x --name iot_dynamodb_messages

# parameter store (unused)
aws ssm put-parameter \
  --name /iot_demo/table_name \
  --type String \
  --value "IotDemo" \
  --description "DynamoDB Table name" \
  --overwrite

# validate
sam validate --template template.yaml
aws cloudformation validate-template \
  --template-body file://template.yaml

# build, package, deploy
time sam build

time sam package \
    --output-template-file packaged.yaml \
    --s3-bucket gstafford-sam-demo

time sam deploy --template-file packaged.yaml \
  --stack-name iot-dynamodb \
  --capabilities CAPABILITY_IAM

export AWS_REGION=us-east-1
export S3_BUCKET=gstafford-iot-data
export TABLE_NAME=iot-dynamodb-IotDemoTable-DBSDROSJ2FKQ
export SQS_QUEUE_ARN=arn:aws:sqs:us-east-1:931066906971:iot-dynamodb-IotDemoQueue-13GR2RRF67YD0
export QUEUE_URL=https://sqs.us-east-1.amazonaws.com/931066906971/iot-dynamodb-IotDemoQueue-13GR2RRF67YD0

# local testing (All CRUD functions)
sam local invoke PostMessageFunction \
  --event iot_dynamodb_messages/event_postMessage.json
sam local invoke GetMessageFunction \
  --event iot_dynamodb_messages/event_getMessage.json
sam local invoke GetMessagesFunction \
  --event iot_dynamodb_messages/event_getMessages.json
sam local invoke PutMessageFunction \
  --event iot_dynamodb_messages/event_putMessage.json
sam local invoke DeleteMessageFunction \
  --event iot_dynamodb_messages/event_deleteMessage.json

cd iot_sqs_to_dynamodb/tests/unit
pytest test_handler.py \
  --disable-warnings  --log-level debug \
  --log-file=./log.txt  --verbose
cat log.txt
cd -

python3 ./util_scripts/send_message_sqs.py

# write to s3
aws sqs purge-queue --queue-url $QUEUE_URL
aws s3 cp util_scripts/iot_data.csv s3://$S3_BUCKET

# delete stack
aws cloudformation delete-stack --stack-name iot-dynamodb
```