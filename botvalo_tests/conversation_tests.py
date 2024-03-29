import pytest

import bot_components.gestore as gestore
from bot_components.db.db_manager import Database
from bot_components.foto import Foto
from bot_components.insulti import Insulti
from bot_components.menu import Menu
from bot_components.risposte import Risposte
from botvalo_tests.framework.mockbot import MockBot
from botvalo_tests.framework.mockcontext import MockContext
from botvalo_tests.framework.mockdatabase import MockDatabase
from botvalo_tests.framework.mockdispatcher import MockDispatcher
from botvalo_tests.framework.mockupdate import MockUpdate
from botvalo_tests.test_utilities.common_tests_utils import *

bot = MockBot()
dispatcher = MockDispatcher(bot)
context = MockContext(dispatcher)
db: MockDatabase = None


@pytest.fixture(scope="module", autouse=True)
def module_setup():
    Database.set_db_type(MockDatabase)
    local_db: MockDatabase = Database.get()
    local_db.load_default_values()
    Risposte.init()
    Insulti.init()
    Foto.init()
    SET_COMMON_BOT(bot)
    global db
    db = local_db


def test_Insulti_ifNonTriggerMessage_ShouldNotReply(simple_setup):
    send_fake_message_to(Insulti, "non_trigger")
    assert len(bot.result) == 0


def test_Insulti_ifTriggerMessage_ShouldReplyWithInsult(simple_setup):
    send_fake_message_to(Insulti, "insulta {}")
    res = bot.result
    assert len(res) == 1
    assert 'text' in res[0]
    assert res[0].get('text') in Insulti.lista_insulti


def test_Foto_ifTriggerWordSent_ShouldSendPhoto(empty_blacklist):
    send_fake_message_to(Foto, "mazza")
    assert len(bot.result) == 1
    assert has_valid_photo(bot.result)


def test_Foto_ifNonTriggerWordSent_ShouldNotSendPhoto(simple_setup):
    send_fake_message_to(Foto, "non_trigger")
    assert len(bot.result) == 0


def test_Foto_ifTextContainsTrigger_ShouldSendPhoto(empty_blacklist):
    send_fake_message_to(Foto, "test mazza test")
    assert len(bot.result) == 1
    assert has_valid_photo(bot.result)


def test_Foto_ifTextContainsTriggerWithPunctuation_ShouldSendPhoto(empty_blacklist):
    send_fake_message_to(Foto, "test, mazza, test")
    assert len(bot.result) == 1
    assert has_valid_photo(bot.result, 0)
    send_fake_message_to(Foto, "test...mazza? Test.")
    assert len(bot.result) == 2
    assert has_valid_photo(bot.result, 1)


def test_Foto_ifTextContainsNonExplicitTrigger_ShouldNotSendPhoto(empty_blacklist):
    send_fake_message_to(Foto, "testmazzatest")
    assert len(bot.result) == 0


def test_Foto_setChatRemovalTimer():
    test_chat = MockChat(1234)
    Foto.set_chat_removal_timer(test_chat, 30)
    assert db.get_chat_removal_seconds(test_chat.id) == 30


def test_Foto_deletePhoto():
    mes = MockMessage("")
    Foto._delete_message(mes)
    assert mes._deleted is True


# noinspection PyTypeChecker
def test_Risposte_ifTextContainsTriggerWithPunctuation_ShouldReply(simple_setup):
    update1 = MockUpdate.from_message("test, grazie, test")
    update2 = MockUpdate.from_message("test...grazie? Test.")
    update3 = MockUpdate.from_message("test...GrAzIe!Test.")
    gestore.inoltra_messaggio(update1)
    assert len(bot.result) == 1
    gestore.inoltra_messaggio(update2)
    assert len(bot.result) == 2
    gestore.inoltra_messaggio(update3)
    send_fake_message_to(Foto, "test...grazie! Test.")
    assert len(bot.result) == 3


def test_Risposte_ifTriggerWordSent_ShouldReply(simple_setup):
    send_fake_message_to(Risposte, "grazie")
    assert len(bot.result) == 1


def test_Risposte_ifNonTriggerWordSent_ShouldNotReply(simple_setup):
    send_fake_message_to(Risposte, "non_trigger")
    assert len(bot.result) == 0


def test_Risposte_ifTextContainsExplicitTrigger_ShouldReply(simple_setup):
    send_fake_message_to(Risposte, "davvero grazie mille")
    assert len(bot.result) == 1


def test_Risposte_alternativeTextValue(simple_setup):
    send_fake_message_to(Risposte, "ricorsione")
    send_fake_message_to(Risposte, "ricorsivo")
    assert len(bot.result) == 2
    assert bot.result[0]['text'] == bot.result[1]['text']


# noinspection PyTypeChecker
def test_Gestore_ifHourInBlacklist_ShouldNotSendPhoto(full_blacklist):
    assert Foto.hour_in_blacklist()
    update = MockUpdate.from_message("mazza")
    gestore.inoltra_messaggio(update, context)
    assert len(bot.result) == 0


# noinspection PyTypeChecker
def test_Gestore_ifHourInBlacklist_ShouldStillSendTextMessages(full_blacklist):
    update_risposte = MockUpdate.from_message("grazie")
    gestore.inoltra_messaggio(update_risposte, context)
    assert len(bot.result) == 1
    assert "text" in bot.result[0]
    update_insulti = MockUpdate.from_message("insulta Test")
    gestore.inoltra_messaggio(update_insulti, context)
    assert len(bot.result) == 2
    assert "text" in bot.result[1]


# noinspection PyTypeChecker
def test_ifMoreCategoriesAreTriggered_ShouldSendMultipleMessages(empty_blacklist):
    update = MockUpdate.from_message("grazie insulta Test")
    gestore.inoltra_messaggio(update, context)
    assert len(bot.result) == 2
    bot.reset_data()
    update = MockUpdate.from_message("mazza grazie")
    gestore.inoltra_messaggio(update, context)
    assert len(bot.result) == 2


def test_onMenuCommand_ShouldSendMenu(simple_setup):
    from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
    update = MockUpdate.empty()
    Menu.show(update)
    res = bot.result
    assert len(res) == 1
    assert 'reply_markup' in res[0]
    assert type(res[0]['reply_markup']) is InlineKeyboardMarkup
