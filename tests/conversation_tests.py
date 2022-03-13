import pytest

import bot_components.gestore as gestore
from bot_components.db.db_manager import Database
from bot_components.foto import Foto
from bot_components.insulti import Insulti
from bot_components.menu import Menu
from bot_components.risposte import Risposte
from tests.framework.mockbot import MockBot
from tests.framework.mockcontext import MockContext
from tests.framework.mockdatabase import MockDatabase
from tests.framework.mockdispatcher import MockDispatcher
from tests.framework.mockupdate import MockUpdate
# noinspection PyUnresolvedReferences
from tests.test_utilities.common_fixtures import *
from tests.test_utilities.common_tests_utils import *

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


def test_Gestore_ifMessageEdited_ShouldNotReply(simple_setup):
    update = MockUpdate.from_message("test")
    update._edit_message("mazza")
    gestore.inoltra_messaggio(update)
    assert len(bot.result) == 0


def test_Gestore_ifMessageIsTimerCommand_ShouldChangeChatPhotoRemovalTimer(simple_setup):
    TEST_CHAT_ID = -234410
    TEST_CHAT = MockChat(TEST_CHAT_ID)

    update1 = MockUpdate.from_message("botvalo timer 20")
    update1._chat = TEST_CHAT
    gestore.inoltra_messaggio(update1)
    assert str(TEST_CHAT_ID) in db.removal_seconds
    assert db.get_chat_removal_seconds(TEST_CHAT_ID) == 20

    update2 = MockUpdate.from_message("botvalo timer 5.7")
    update2._chat = TEST_CHAT
    gestore.inoltra_messaggio(update2)
    assert db.get_chat_removal_seconds(TEST_CHAT_ID) == 5.7


def test_Foto_onTimerCommandWithoutParameters_ShouldNotChangeChatPhotoRemovalTimer(simple_setup):
    TEST_CHAT_ID = -234410
    db.set_chat_removal_seconds(TEST_CHAT_ID, 1752)

    update = MockUpdate.from_message("botvalo timer")
    update._chat = MockChat(TEST_CHAT_ID)
    gestore.inoltra_messaggio(update)
    assert db.get_chat_removal_seconds(TEST_CHAT_ID) == 1752
    assert len(bot.result) == 1
    assert "1752" in bot.result[0]['text']


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
