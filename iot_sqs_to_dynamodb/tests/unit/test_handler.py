from ... import app


def test_lambda_handler_post(post_event):
    ret = app.lambda_handler(post_event, None)
    assert ret == 0


def test_lambda_handler_put(put_event):
    ret = app.lambda_handler(put_event, None)
    assert ret == 0


def test_lambda_handler_get(get_event):
    ret = app.lambda_handler(get_event, None)
    assert ret == 0


def test_lambda_handler_get_all(get_all_event):
    ret = app.lambda_handler(get_all_event, None)
    assert ret == 0


def test_lambda_handler_delete(delete_event):
    ret = app.lambda_handler(delete_event, None)
    assert ret == 0
