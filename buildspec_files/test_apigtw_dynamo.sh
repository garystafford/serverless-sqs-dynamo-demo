#!/usr/bin/env bash

# Integration tests: Produces SQS events that trigger Lambda
# Events contain CRUD commands for DynamoDB

#set -x

pushd iot_dynamodb_messages/events || exit

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
