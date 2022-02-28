import os

import pytest

import bot_components.gestore as gestore
from tests.framework.mockbot import MockBot
from utils.os_utils import *

# noinspection PyTypeChecker
COMMON_BOT: MockBot = None


def SET_COMMON_BOT(bot):
    global COMMON_BOT
    COMMON_BOT = bot


@pytest.fixture
def setup():
    COMMON_BOT.reset_data()


@pytest.fixture
def full_blacklist():
    setup_full_blacklist()
    yield
    teardown_fake_blacklist()


@pytest.fixture
def empty_blacklist():
    setup_empty_blacklist()
    yield
    teardown_fake_blacklist()


def setup_full_blacklist():
    COMMON_BOT.reset_data()
    create_fake_blacklist('{"monday": [0, 24], "tuesday": [0, 24], "wednesday": [0, 24],'
                          '"thursday": [0, 24], "friday": [0, 24], "saturday": [0, 24],'
                          '"sunday": [0,24]}')


def setup_empty_blacklist():
    COMMON_BOT.reset_data()
    create_fake_blacklist("{}")


def create_fake_blacklist(text):
    original_name = path_to_text_file("schedule_blacklist.json")
    temp_name = path_to_text_file("temp.json")
    fake_name = path_to_text_file("test_blacklist.json")
    with open(fake_name, 'x') as fake_file:
        fake_file.write(text)
    os.rename(original_name, temp_name)
    os.rename(fake_name, original_name)
    gestore.init_hour_blacklist()
    print("Successfully setupped fake blacklist.")


def teardown_fake_blacklist():
    original_name = path_to_text_file("schedule_blacklist.json")
    temp_name = path_to_text_file("temp.json")
    fake_name = path_to_text_file("test_blacklist.json")

    os.rename(original_name, fake_name)
    os.rename(temp_name, original_name)
    os.remove(fake_name)
    print("Successfully torn down fake blacklist.")
