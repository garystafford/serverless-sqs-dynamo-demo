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

# variables
S3_BUILD_BUCKET="gstafford-sam-demo"
STACK_NAME="serverless-sqs-dynamo-demo"

# validate
sam validate --template template.yaml

aws cloudformation validate-template \
  --template-body file://template.yaml

# build
time sam build --template template.yaml

# package
time sam package \
  --output-template-file packaged.yaml \
  --s3-bucket "${S3_BUILD_BUCKET}"

# deploy
time sam deploy --template-file packaged.yaml \
  --stack-name "${STACK_NAME}" \
  --capabilities CAPABILITY_IAM \
  --debug

AWS_REGION=us-east-1
S3_DATA_BUCKET=gstafford-demo-data
SQS_QUEUE_ARN=arn:aws:sqs:us-east-1:931066906971:serverless-sqs-dynamo-demo-DemoQueue-10Q1K9DRH7510
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/931066906971/serverless-sqs-dynamo-demo-DemoQueue-10Q1K9DRH7510

# variables (required by local lambda functions)
TABLE_NAME=serverless-sqs-dynamo-demo-DemoTable-1AFWJE2O1N0IR

# local testing (All CRUD functions)
sam local invoke PostMessageFunction \
  --event lambda_apigtw_to_dynamodb/events/event_postMessage.json
sam local invoke GetMessageFunction \
  --event lambda_apigtw_to_dynamodb/events/event_getMessage.json
sam local invoke GetMessagesFunction \
  --event lambda_apigtw_to_dynamodb/events/event_getMessages.json
sam local invoke PutMessageFunction \
  --event lambda_apigtw_to_dynamodb/events/event_putMessage.json
sam local invoke DeleteMessageFunction \
  --event lambda_apigtw_to_dynamodb/events/event_deleteMessage.json

cd lambda_sqs_to_dynamodb/tests/unit
pytest test_handler.py \
  --disable-warnings  --log-level debug \
  --log-file=./log.txt  --verbose
cat log.txt
cd -

python3 ./util_scripts/send_message_sqs.py

# write to s3
aws sqs purge-queue --queue-url $QUEUE_URL
aws s3 cp sample_data/data.csv s3://$S3_DATA_BUCKET

# delete stack
aws s3 rm s3://$S3_DATA_BUCKET/data.csv
aws cloudformation delete-stack \
  --stack-name serverless-sqs-dynamo-demo
```

```text
.
├── README.md
├── iot_api_to_dynamodb
│   ├── app.js
│   ├── events
│   ├── node_modules
│   ├── package.json
│   └── tests
├── iot_s3_to_sqs
│   ├── __init__.py
│   ├── app.py
│   ├── requirements.txt
│   └── tests
├── iot_sqs_to_dynamodb
│   ├── __init__.py
│   ├── app.py
│   ├── requirements.txt
│   └── tests
├── requirements.txt
├── template.yaml
└── sample_data
    ├── iot_data.csv
    ├── iot_data_bad_msg.csv
    └── iot_data_good_msg.csv
```
