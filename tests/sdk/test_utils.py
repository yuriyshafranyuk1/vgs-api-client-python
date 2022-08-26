import os
import tempfile
import time

import pytest

from vgs.sdk.errors import NoSuchFileOrDirectoryError
from vgs.sdk.utils import to_json, silent_file_remove, is_file_accessible, read_file, expired


def test_expired():
    sep_13_2020 = 1600000000
    now_plus_10_sec = time.time() + 10
    now_plus_minute = time.time() + 60

    assert expired(sep_13_2020)
    assert expired(now_plus_10_sec)
    assert not expired(now_plus_minute)
    assert expired(now_plus_minute, 60)


def test_file_accessible():
    __assert_write_file(lambda temp_file_path: is_file_accessible(temp_file_path, "w+"))


def test_file_not_accessible_mode():
    __assert_write_file(lambda temp_file_path: not is_file_accessible(temp_file_path, "x"))


def test_file_not_accessible():
    assert not is_file_accessible(__create_temp_file_path())


def test_silent_file_remove():
    file_name = "test_silent_file_remove"
    __create_temp_file_path(file_name)
    silent_file_remove(file_name)


def test_converts_to_json():
    body = __init_json_body('{"test":1}')
    json = to_json(body)
    assert json is not None
    assert json["test"] == 1


def test_throws_ex_on_invalid_json():
    with pytest.raises(Exception):
        body = __init_json_body('{"test":1')
        to_json(body)


def test_throws_ex_on_non_existing_file():
    with pytest.raises(NoSuchFileOrDirectoryError):
        read_file("service_accountzz.yaml")


def test_reads_file():
    temp_dir = tempfile.gettempdir()
    file_name = "test_silent_file"
    full_path = os.path.join(temp_dir, file_name)
    try:
        with open(full_path, "w+") as tmp:
            tmp.write("test")
            content = read_file(file_name, temp_dir)
            assert content is not None
    finally:
        os.remove(full_path)


def __init_json_body(json_str):
    class Body:
        text = ""

    json_text = json_str
    body = Body()
    body.text = json_text
    return body


def __create_temp_file_path(filename="test_file"):
    temp_dir = tempfile.gettempdir()

    return os.path.join(temp_dir, filename)


def __assert_write_file(assertion):
    temp_file_path = __create_temp_file_path()

    try:
        with open(temp_file_path, "w+") as tmp:
            tmp.write("test")

            assert assertion(temp_file_path)
    finally:
        os.remove(temp_file_path)
