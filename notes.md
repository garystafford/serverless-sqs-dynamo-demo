```bash
sam init --runtime nodejs10.x --name iot_dynamodb_getMessage

sam local invoke getMessagesFunction --event event.json

sam package \
    --output-template-file packaged.yaml \
    --s3-bucket gstafford-sam-demo

sam deploy --template-file packaged.yaml \
  --stack-name iot-dynamodb \
  --capabilities CAPABILITY_IAM

aws ssm put-parameter \
  --name /sam_demo/table_name \
  --type String \
  --value "myPets" \
  --description "DynamoDB Table name" \
  --overwrite
```