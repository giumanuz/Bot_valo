import pytest
import telegram.error

from bot_components.commands_registration import CommandRegister
from bot_components.foto import Foto
from bot_components.menu import Menu
from botvalo_tests.framework.mockbot import MockBot
from botvalo_tests.framework.mockchat import MockChat
from botvalo_tests.framework.mockdispatcher import MockDispatcher
from botvalo_tests.framework.mockmessage import MockMessage


def test_Menu_shouldAddCommandHandler_WhenInit():
    from telegram.ext import CommandHandler
    d = MockDispatcher(MockBot())
    CommandRegister.init(d)
    Menu.init(d)
    assert len(d.handlers) == 1
    ch: CommandHandler = d.handlers[0]
    assert isinstance(ch, CommandHandler)
    assert ch.command[0] == "menu"
    assert ch.callback == Menu.show


def test_Foto_ifRemovalSecondsNotValid_ShouldThrowTypeError():
    with pytest.raises(TypeError):
        chat_id = 1243
        chat = MockChat(chat_id)
        Foto.set_chat_removal_timer(chat, "error")
    with pytest.raises(TypeError):
        Foto.set_chat_removal_timer("Test", 123)


def test_Foto_listContainsText():
    lst = ["this", "is", "a", "test"]
    assert Foto._text_in_list("test", lst)
    assert not Foto._text_in_list("testing", lst)


def test_Foto_doesNotRaiseError_WhenMessageCannotBeDeleted():
    mes = MockMessage("")
    mes._set_exception_on_delete(telegram.error.BadRequest(""))
    Foto._delete_message(mes)
    assert mes._deleted is False
    mes._set_exception_on_delete(telegram.error.TimedOut())
    Foto._delete_message(mes)
    assert mes._deleted is False
