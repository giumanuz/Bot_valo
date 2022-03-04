import pytest

from tests.test_utilities.common_tests_utils import GET_COMMON_BOT
from utils.os_utils import *


# noinspection PyTypeChecker


@pytest.fixture
def setup():
    GET_COMMON_BOT().reset_data()


@pytest.fixture
def full_blacklist():
    GET_COMMON_BOT().reset_data()
    old_text = setup_full_blacklist()
    yield
    teardown_fake_blacklist(old_text)


def setup_full_blacklist():
    return create_blacklist_and_get_old_text(
        '{"monday": [0, 24], "tuesday": [0, 24], "wednesday": [0, 24], "thursday": [0, 24],'
        '"friday": [0, 24], "saturday": [0, 24],"sunday": [0,24]}')


@pytest.fixture
def empty_blacklist():
    GET_COMMON_BOT().reset_data()
    old_text = setup_empty_blacklist()
    yield
    teardown_fake_blacklist(old_text)


def setup_empty_blacklist():
    return create_blacklist_and_get_old_text("{}")


def create_blacklist_and_get_old_text(new_text):
    path_to_json = path_to_text_file("schedule_blacklist.json")
    with open(path_to_json, 'r') as f:
        pre_text = f.read()
    with open(path_to_json, 'w') as f:
        f.write(new_text)
        return pre_text


def teardown_fake_blacklist(pre_text):
    with open(path_to_text_file("schedule_blacklist.json"), 'w') as f:
        f.write(pre_text)
