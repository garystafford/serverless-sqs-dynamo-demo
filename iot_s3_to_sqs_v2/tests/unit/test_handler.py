import os

from ... import app


# def test_lambda_handler(apigw_event, mocker):
#     ret = app.lambda_handler(apigw_event, "")
#     assert ret == 0


def test_process_messages(messages):
    ret = app.process_messages(messages)
    assert ret == 0


def test_convert_message(message_string):
    ret = app.convert_message(message_string)
    assert ret['TableName'] == os.getenv("TABLE_NAME")
    assert len(ret.keys()) == 2


# def test_send_sqs_message(message_json):
#     ret = app.send_sqs_message(message_json)
#     assert ret is not None




