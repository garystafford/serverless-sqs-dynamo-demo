```bash
sam init --runtime nodejs10.x --name iot_dynamodb_getMessage

aws ssm put-parameter \
  --name /iot_demo/table_name \
  --type String \
  --value "IotDemo" \
  --description "DynamoDB Table name" \
  --overwrite

sam validate --template template.yaml
aws cloudformation validate-template \
  --template-body file://template.yaml

sam package \
    --output-template-file packaged.yaml \
    --s3-bucket gstafford-sam-demo

sam deploy --template-file packaged.yaml \
  --stack-name iot-dynamodb \
  --capabilities CAPABILITY_IAM

export TABLE_NAME=iot-dynamodb-IotDemoTable-1E1VFYADYIPIL
sam local invoke GetMessageFunction --event event_getMessage.json
sam local invoke GetMessagesFunction --event event_getMessages.json
sam local invoke PostMessageFunction --event event_postMessage.json

export QUEUE_URL=https://sqs.us-east-1.amazonaws.com/931066906971/iot-dynamodb-IotDemoQueue-XYWKCFK3DC6C
python3 ./util_scripts/send_message_sqs.py

export TABLE_NAME=gstafford-ml-sensor-data

cd /iot_sqs_to_dynamodb/tests
pytest ./test_handler.py --disable-warnings

aws s3 cp util_scripts/iot_data.csv \
  s3://gstafford-ml-sensor-data/iot_dynamodb_demo/

aws cloudformation delete-stack --stack-name iot-dynamodb

aws s3 cp iot_data.csv s3://gstafford-iot-data
```