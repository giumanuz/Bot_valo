import pytest

from bot_components.menu import Menu
from tests.framework.mockdispatcher import MockDispatcher


@pytest.fixture
def reset_menu():
    Menu.buttons_list = []


def test_Menu_shouldAddCommandHandler_WhenInit():
    from telegram.ext import CommandHandler
    d = MockDispatcher(None)
    Menu.init(d)
    assert len(d.handlers) == 1
    ch: CommandHandler = d.handlers[0]
    assert isinstance(ch, CommandHandler)
    assert ch.command[0] == "menu"
    assert ch.callback == Menu.show


def test_Menu_whenListIsEmpty_AddsCommandToList(reset_menu):
    assert len(Menu.buttons_list) == 0
    Menu.register_button("test", "callback-test")
    assert len(Menu.buttons_list) == 1
    assert len(Menu.buttons_list[0]) == 1
    assert Menu.buttons_list[0][0].text == "test"
    assert Menu.buttons_list[0][0].callback_data == "callback-test"


def test_Menu_createsListIfLimitReached(reset_menu):
    Menu.buttons_list = [[0]]
    Menu.register_button("a", "")
    assert len(Menu.buttons_list) == 1
    assert len(Menu.buttons_list[0]) == 2
    Menu.register_button("b", "")
    assert len(Menu.buttons_list) == 2
    assert len(Menu.buttons_list[1]) == 1
    Menu.register_button("c", "")
    assert len(Menu.buttons_list) == 2
    assert len(Menu.buttons_list[1]) == 2
