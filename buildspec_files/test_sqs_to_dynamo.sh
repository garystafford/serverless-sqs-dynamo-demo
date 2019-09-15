#!/usr/bin/env bash

# Integration tests: Produces SQS events that trigger Lambda
# Events contain CRUD commands for DynamoDB

#set -x

export AWS_REGION
export TABLE_NAME
export SQS_QUEUE_ARN

pushd iot_sqs_to_dynamodb/tests/unit || exit

pytest test_handler.py \
  --disable-warnings  --log-level debug
# --log-file=./log.txt  --verbose

#cat log.txt