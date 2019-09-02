import json
import os

from ... import app


def test_convert_message(message):
    ret = app.convert_message(message)
    assert ret['TableName'] == os.getenv("TABLE_NAME")


def test_lambda_handler(apigw_event, mocker):
    ret = app.lambda_handler(apigw_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "message" in ret["body"]
    assert data["message"] == "hello world"
    # assert "location" in data.dict_keys()
