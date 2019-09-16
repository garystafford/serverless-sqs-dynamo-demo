#!/usr/bin/env bash

# Integration tests: Produces SQS events that trigger Lambda
# Events contain CRUD commands for DynamoDB

#set -x

pushd iot_api_to_dynamodb || exit

ls -alh

# local testing (All CRUD functions)
sam local invoke PostMessageFunction \
  --event events/event_postMessage.json

sam local invoke GetMessageFunction \
  --event events/event_getMessage.json

sam local invoke GetMessagesFunction \
  --event events/event_getMessages.json

sam local invoke PutMessageFunction \
  --event events/event_putMessage.json

sam local invoke DeleteMessageFunction \
  --event events/event_deleteMessage.json
