import pytest

from bot_components.foto import Foto
from bot_components.insulti import Insulti
from bot_components.menu import Menu
from bot_components.risposte import Risposte
from tests.framework.mock_update_factory import MockUpdateFactory
from tests.framework.mocks import *

bot = MockBot()
dispatcher = MockDispatcher(bot)
context = MockContext(dispatcher)


@pytest.fixture
def setup():
    bot.reset_data()


def test_Insulti_ifNonTriggerMessage_ShouldNotReply(setup):
    res = _send_fake_message_to(Insulti, "non_trigger")
    assert len(res) == 0


def test_Insulti_ifTriggerMessage_ShouldReplyWithInsult(setup):
    res = _send_fake_message_to(Insulti, "insulta")
    assert len(res) == 1
    assert 'text' in res[0]
    assert res[0].get('text')[7:] in Insulti.lista_insulti


def test_Foto_ifTriggerWordSent_ShouldSendPhoto(setup):
    res = _send_fake_message_to(Foto, "mazza")
    assert len(res) == 1
    assertHasValidPhoto(res)
    bot.reset_data()


def test_Foto_ifNonTriggerWordSent_ShouldNotSendPhoto(setup):
    res = _send_fake_message_to(Foto, "non_trigger")
    assert len(res) == 0


def test_Foto_ifTextContainsTrigger_ShouldSendPhoto(setup):
    res = _send_fake_message_to(Foto, "test mazza test")
    assert len(res) == 1
    assertHasValidPhoto(res)


def test_Risposte_ifTextContainsNonExplicitTrigger_ShouldNotSendPhoto(setup):
    res = _send_fake_message_to(Foto, "testmazzatest")
    assert len(res) == 0


def test_onMenuCommand_ShouldSendMenu(setup):
    from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
    update = MockUpdateFactory.empty()
    Menu.handle_command(update, context)
    res = bot.result
    assert len(res) == 1
    assert 'reply_markup' in res[0]
    assert type(res[0]['reply_markup']) is InlineKeyboardMarkup


def test_Risposte_ifTriggerWordSent_ShouldReply(setup):
    res = _send_fake_message_to(Risposte, "test")
    assert len(res) == 1


def test_Risposte_ifNonTriggerWordSent_ShouldNotReply(setup):
    res = _send_fake_message_to(Risposte, "non_trigger")
    assert len(res) == 0


def test_Risposte_ifTextContainsExplicitTrigger_ShouldReply(setup):
    res = _send_fake_message_to(Risposte, "this is a test")
    assert len(res) == 1


def _send_fake_message_to(cls, text):
    update = MockUpdateFactory.with_message(text)
    cls.handle_message(update, context)
    return bot.result


def assertHasValidPhoto(res):
    assert 'photo' in res[0]
    assert len(res[0]['photo']) != 0
