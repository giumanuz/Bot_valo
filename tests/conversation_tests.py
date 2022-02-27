import os

import pytest

import bot_components.gestore as gestore
from bot_components.foto import Foto
from bot_components.insulti import Insulti
from bot_components.menu import show_menu
from bot_components.risposte import Risposte
from bot_components.utils.os_utils import path_to_text_file
from tests.framework.mockbot import MockBot
from tests.framework.mockcontext import MockContext
from tests.framework.mockdispatcher import MockDispatcher
from tests.framework.mockupdate import MockUpdate

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
    assert _has_valid_photo(res)
    bot.reset_data()


def test_Foto_ifNonTriggerWordSent_ShouldNotSendPhoto(setup):
    res = _send_fake_message_to(Foto, "non_trigger")
    assert len(res) == 0


def test_Foto_ifTextContainsTrigger_ShouldSendPhoto(setup):
    res = _send_fake_message_to(Foto, "test mazza test")
    assert len(res) == 1
    assert _has_valid_photo(res)


@pytest.mark.skip(reason="da implementare, non urgente")  # TODO
def test_Foto_ifTextContainsTriggerWithPunctuation_ShouldSendPhoto(setup):
    res = _send_fake_message_to(Foto, "test, mazza, test")
    assert len(res) == 1
    assert _has_valid_photo(res, 0)
    _send_fake_message_to(Foto, "test...mazza? Test.")
    assert len(res) == 2
    assert _has_valid_photo(res, 1)


def test_Risposte_ifTextContainsNonExplicitTrigger_ShouldNotSendPhoto(setup):
    res = _send_fake_message_to(Foto, "testmazzatest")
    assert len(res) == 0


def test_onMenuCommand_ShouldSendMenu(setup):
    from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
    update = MockUpdate.empty()
    show_menu(update, context)
    res = bot.result
    assert len(res) == 1
    assert 'reply_markup' in res[0]
    assert type(res[0]['reply_markup']) is InlineKeyboardMarkup


def test_Risposte_ifTriggerWordSent_ShouldReply(setup):
    res = _send_fake_message_to(Risposte, "grazie")
    assert len(res) == 1


def test_Risposte_ifNonTriggerWordSent_ShouldNotReply(setup):
    res = _send_fake_message_to(Risposte, "non_trigger")
    assert len(res) == 0


def test_Risposte_ifTextContainsExplicitTrigger_ShouldReply(setup):
    res = _send_fake_message_to(Risposte, "davvero grazie mille")
    assert len(res) == 1


@pytest.fixture
def setup_fake_blacklist():
    bot.reset_data()

    original_name = path_to_text_file("schedule_blacklist.json")
    temp_name = path_to_text_file("temp.json")
    fake_name = path_to_text_file("test_blacklist.json")

    with open(fake_name, 'x') as fake_file:
        fake_file.write('{"monday": [0, 24], "tuesday": [0, 24], "wednesday": [0, 24],'
                        '"thursday": [0, 24], "friday": [0, 24]}')

    os.rename(original_name, temp_name)
    os.rename(fake_name, original_name)
    gestore.init_hour_blacklist()


@pytest.fixture
def teardown_fake_blacklist():
    original_name = path_to_text_file("schedule_blacklist.json")
    temp_name = path_to_text_file("temp.json")
    fake_name = path_to_text_file("test_blacklist.json")
    os.rename(original_name, fake_name)
    os.rename(temp_name, original_name)
    os.remove(fake_name)


def test_Gestore_ifHourInBlacklist_ShouldNotSendPhoto(setup_fake_blacklist, teardown_fake_blacklist):
    update = MockUpdate.from_message("mazza")
    gestore._inoltra_messaggio(update, context)
    assert len(bot.result) == 0


def test_Gestore_ifHourInBlacklist_ShouldStillSendTextMessages(setup_fake_blacklist, teardown_fake_blacklist):
    update_risposte = MockUpdate.from_message("grazie")
    gestore._inoltra_messaggio(update_risposte, context)
    assert len(bot.result) == 1
    assert "text" in bot.result[0]
    update_insulti = MockUpdate.from_message("insulta")
    gestore._inoltra_messaggio(update_insulti, context)
    assert len(bot.result) == 2
    assert "text" in bot.result[1]


@pytest.mark.skip(reason="da implementare, non urgente")  # TODO
def test_ifMoreCategoriesAreTriggered_ShouldSendMultipleMessages(setup):
    update = MockUpdate.from_message("mazza grazie")
    gestore._inoltra_messaggio(update, context)
    assert len(bot.result) == 2


def _send_fake_message_to(cls, text):
    update = MockUpdate.from_message(text)
    cls.handle_message(update, context)
    return bot.result


def _has_valid_photo(res, index=0):
    return 'photo' in res[index] and len(res[index]['photo']) != 0
