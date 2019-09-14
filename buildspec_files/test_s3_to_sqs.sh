#!/usr/bin/env bash

# Integration tests: Produces SQS events that trigger Lambda
# Events contain CRUD commands for DynamoDB

#set -x

export TABLE_NAME
export S3_BUCKET

pushd iot_s3_to_sqs/tests/unit || exit

pytest test_handler.py \
  --disable-warnings  --log-level debug
# --log-file=./log.txt  --verbose

#cat log.txt