#!/usr/bin/env bash

set -x

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
