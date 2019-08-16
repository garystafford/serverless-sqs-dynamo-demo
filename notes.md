```bash
sam init --runtime nodejs10.x --name iot_dynamodb_getMessage

sam local invoke GetMessageFunction --event event_getMessage.json
sam local invoke GetMessagesFunction --event event_getMessages.json
sam local invoke PostMessageFunction --event event_postMessage.json
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket gstafford-sam-demo

sam deploy --template-file packaged.yaml \
  --stack-name iot-dynamodb \
  --capabilities CAPABILITY_IAM

aws ssm put-parameter \
  --name /iot_demo/table_name \
  --type String \
  --value "IotDemoTable" \
  --description "DynamoDB Table name" \
  --overwrite

sam validate --template template.yaml
aws cloudformation validate-template \
  --template-body file://template.yaml
```