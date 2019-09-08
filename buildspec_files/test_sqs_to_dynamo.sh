#!/usr/bin/env bash

# Test SQS to DynamoDB

#set -x

export AWS_REGION
export TABLE_NAME
export SQS_QUEUE

ls -alh

pushd iot_sqs_to_dynamodb/tests/unit || exit

ls -alh

pytest test_handler.py \
  --disable-warnings  --log-level debug \
  --log-file=./log.txt  --verbose

cat log.txt

popd || exit