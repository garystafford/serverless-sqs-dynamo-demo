import os

from ... import app


def test_lambda_handler_returns_0(post_event):
    ret = app.lambda_handler(post_event, None)
    assert ret == 0


def test_process_messages_returns_0(messages):
    ret = app.process_messages(messages)
    assert ret == 0


def test_convert_message_returns_two_keys(message_string):
    ret = app.convert_message(message_string)
    assert len(ret.keys()) == 2


def test_convert_message_returns_correct_table(message_string):
    ret = app.convert_message(message_string)
    assert ret['TableName'] == os.getenv("TABLE_NAME")


def test_send_sqs_message_returns_none(message_json):
    ret = app.send_sqs_message(message_json)
    assert ret is not None




