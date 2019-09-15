#!/usr/bin/env bash

# Build, package, deploy sam template containing all resources

#set -x

export S3_BUCKET_BUILD

# validate
sam validate --template template.yaml
aws cloudformation validate-template \
  --template-body file://template.yaml

# build, package, deploy
time sam build

time sam package \
  --output-template-file packaged.yaml \
  --s3-bucket "${S3_BUCKET_BUILD}"

time sam deploy \
  --template-file packaged.yaml \
  --stack-name iot-dynamodb \
  --capabilities CAPABILITY_IAM \
  --debug

# catch error - cloudformation returns code 255
# (exit non-zero) if stack exists and no updates
if [ "$?" -eq 255 ]
then
    echo "No changes to deploy."
    true
fi