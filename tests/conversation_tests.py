from bot_components.foto import Foto
from bot_components.insulti import Insulti
from bot_components.menu import show_menu
from bot_components.risposte import Risposte
from tests.framework.mockcontext import MockContext
from tests.framework.mockdispatcher import MockDispatcher
from tests.test_utilities.common_fixtures import *
from tests.test_utilities.common_tests_utils import *

bot = MockBot()
dispatcher = MockDispatcher(bot)
context = MockContext(dispatcher)

SET_COMMON_BOT(bot)
SET_COMMON_CONTEXT(context)


def test_Insulti_ifNonTriggerMessage_ShouldNotReply(setup):
    send_fake_message_to(Insulti, "non_trigger")
    assert len(bot.result) == 0


def test_Insulti_ifTriggerMessage_ShouldReplyWithInsult(setup):
    send_fake_message_to(Insulti, "insulta")
    res = bot.result
    assert len(res) == 1
    assert 'text' in res[0]
    assert res[0].get('text')[7:] in Insulti.lista_insulti


def test_Foto_ifTriggerWordSent_ShouldSendPhoto(setup):
    send_fake_message_to(Foto, "mazza")
    assert len(bot.result) == 1
    assert has_valid_photo(bot.result)


def test_Foto_ifNonTriggerWordSent_ShouldNotSendPhoto(setup):
    send_fake_message_to(Foto, "non_trigger")
    assert len(bot.result) == 0


def test_Foto_ifTextContainsTrigger_ShouldSendPhoto(setup):
    send_fake_message_to(Foto, "test mazza test")
    assert len(bot.result) == 1
    assert has_valid_photo(bot.result)


def test_Foto_ifTextContainsTriggerWithPunctuation_ShouldSendPhoto(setup):
    send_fake_message_to(Foto, "test, mazza, test")
    assert len(bot.result) == 1
    assert has_valid_photo(bot.result, 0)
    send_fake_message_to(Foto, "test...mazza? Test.")
    assert len(bot.result) == 2
    assert has_valid_photo(bot.result, 1)
    send_fake_message_to(Foto, "test...MaZzA! Test.")
    assert len(bot.result) == 3
    assert has_valid_photo(bot.result, 2)


# noinspection PyTypeChecker
def test_Risposte_ifTextContainsTriggerWithPunctuation_ShouldReply(setup):
    update1 = MockUpdate.from_message("test, grazie, test")
    update2 = MockUpdate.from_message("test...grazie? Test.")
    update3 = MockUpdate.from_message("test...GrAzIe!Test.")
    gestore._inoltra_messaggio(update1, context)
    assert len(bot.result) == 1
    gestore._inoltra_messaggio(update2, context)
    assert len(bot.result) == 2
    gestore._inoltra_messaggio(update3, context)
    send_fake_message_to(Foto, "test...grazie! Test.")
    assert len(bot.result) == 3


def test_Risposte_ifTextContainsNonExplicitTrigger_ShouldNotSendPhoto(setup):
    send_fake_message_to(Foto, "testmazzatest")
    assert len(bot.result) == 0


def test_onMenuCommand_ShouldSendMenu(setup):
    from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
    update = MockUpdate.empty()
    show_menu(update, context)
    res = bot.result
    assert len(res) == 1
    assert 'reply_markup' in res[0]
    assert type(res[0]['reply_markup']) is InlineKeyboardMarkup


def test_Risposte_ifTriggerWordSent_ShouldReply(setup):
    send_fake_message_to(Risposte, "grazie")
    assert len(bot.result) == 1


def test_Risposte_ifNonTriggerWordSent_ShouldNotReply(setup):
    send_fake_message_to(Risposte, "non_trigger")
    assert len(bot.result) == 0


def test_Risposte_ifTextContainsExplicitTrigger_ShouldReply(setup):
    send_fake_message_to(Risposte, "davvero grazie mille")
    assert len(bot.result) == 1


# noinspection PyTypeChecker
def test_Gestore_ifHourInBlacklist_ShouldNotSendPhoto(full_blacklist):
    assert gestore.hour_in_blacklist()
    update = MockUpdate.from_message("mazza")
    gestore._inoltra_messaggio(update, context)
    assert len(bot.result) == 0


# noinspection PyTypeChecker
def test_Gestore_ifHourInBlacklist_ShouldStillSendTextMessages(full_blacklist):
    update_risposte = MockUpdate.from_message("grazie")
    gestore._inoltra_messaggio(update_risposte, context)
    assert len(bot.result) == 1
    assert "text" in bot.result[0]
    update_insulti = MockUpdate.from_message("insulta")
    gestore._inoltra_messaggio(update_insulti, context)
    assert len(bot.result) == 2
    assert "text" in bot.result[1]


def test_Gestore_ifMessageEdited_ShouldNotReply(setup):
    update = MockUpdate.from_message("test")
    update._edit_message("mazza")
    gestore._inoltra_messaggio(update, context)
    assert len(bot.result) == 0


# noinspection PyTypeChecker
def test_ifMoreCategoriesAreTriggered_ShouldSendMultipleMessages(empty_blacklist):
    update = MockUpdate.from_message("grazie insulta")
    gestore._inoltra_messaggio(update, context)
    assert len(bot.result) == 2
    bot.reset_data()
    update = MockUpdate.from_message("mazza grazie")
    gestore._inoltra_messaggio(update, context)
    assert len(bot.result) == 2
