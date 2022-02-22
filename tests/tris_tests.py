import pytest

from bot_components.games.tris import *
from tests.framework.mockbot import MockBot
from tests.framework.mockcontext import MockContext
from tests.framework.mockdispatcher import MockDispatcher
from tests.framework.mockupdate import MockUpdate
from tests.test_utilities.tris_tests_utils import *

bot = MockBot()
dispatcher = MockDispatcher(bot)
context = MockContext(dispatcher)
tris: Tris

XX = Tris.X_CELL
OO = Tris.O_CELL
NN = Tris.EMPTY_CELL

GIOCATORE_UNO = 111
GIOCATORE_DUE = 222


@pytest.fixture
def simple_setup():
    global tris
    bot.reset_data()
    tris = Tris()
    Tris.active_tris_games = {}


@pytest.fixture
def setup_after_first_turn():
    global tris
    bot.reset_data()
    tris = Tris()
    Tris.active_tris_games = {123: tris}
    tris.message_id = 123
    tris.giocatore_uno = GIOCATORE_UNO
    tris.turno = 2


@pytest.fixture
def setup_after_second_turn():
    global tris
    bot.reset_data()
    tris = Tris()
    Tris.active_tris_games = {123: tris}
    tris.message_id = 123
    tris.giocatore_uno = GIOCATORE_UNO
    tris.giocatore_due = GIOCATORE_DUE
    tris.turno = 1


def test_isTrisShown(simple_setup):
    update = MockUpdate.from_message("")
    Tris.show_tris(update, context)
    res = bot.result
    assert len(res) == 1
    assert 'reply_markup' in res[0]
    assert is_empty_tris(res[0]['reply_markup'])


def test_ifFirstPlayerPresses_putsAnX(simple_setup):
    Tris.active_tris_games = {123: tris}
    update = MockUpdate.create_from(message_id=123, callback_data="tris:0")
    Tris.tris_callback(update, context)
    expected_cells = make_cells(XX, NN, NN,
                                NN, NN, NN,
                                NN, NN, NN)
    assert are_cells_equal(expected_cells, tris.cells)


def test_ifPlayerPresses_editsMessageMarkup(simple_setup):
    Tris.active_tris_games = {123: tris}
    update = MockUpdate.create_from(message_id=123, callback_data="tris:0")
    Tris.tris_callback(update, context)
    assert update.effective_message.reply_markup.inline_keyboard[0][0].text == XX


def test_ifSamePlayerPressesOtherCell_putsAnO(setup_after_first_turn):
    tris.cells = make_cells(XX, NN, NN,
                            NN, NN, NN,
                            NN, NN, NN)
    update = MockUpdate.create_from(callback_data="tris:3", user_id=GIOCATORE_UNO, message_id=123)
    Tris.tris_callback(update, context)
    expected_cells = make_cells(XX, NN, NN,
                                OO, NN, NN,
                                NN, NN, NN)
    assert are_cells_equal(expected_cells, tris.cells)


def test_ifOtherPlayerPressesOtherCell_putsAnO(setup_after_first_turn):
    tris.cells = make_cells(XX, NN, NN,
                            NN, NN, NN,
                            NN, NN, NN)
    update = MockUpdate.create_from(callback_data="tris:3", user_id=GIOCATORE_DUE, message_id=123)
    Tris.tris_callback(update, context)
    expected_cells = make_cells(XX, NN, NN,
                                OO, NN, NN,
                                NN, NN, NN)
    assert are_cells_equal(expected_cells, tris.cells)


def test_ifPlayerTwoPressesInTurnThree_shouldIgnore(setup_after_second_turn):
    tris.cells = expected_cells = make_cells(XX, NN, NN,
                                             OO, NN, NN,
                                             NN, NN, NN)
    update = MockUpdate.create_from(callback_data="tris:5", user_id=GIOCATORE_DUE, message_id=123)
    Tris.tris_callback(update, context)
    assert are_cells_equal(expected_cells, tris.cells)


def test_ifNonPlayerUserPresses_shouldIgnore(setup_after_second_turn):
    tris.cells = expected_cells = make_cells(XX, NN, NN,
                                             OO, NN, NN,
                                             NN, NN, NN)
    update = MockUpdate.create_from(callback_data="tris:5", user_id=789, message_id=123)
    Tris.tris_callback(update, context)
    assert are_cells_equal(expected_cells, tris.cells)


def test_shouldRecognizeWin(simple_setup):
    tris.cells = make_cells(XX, XX, XX,
                            OO, OO, NN,
                            NN, NN, NN)
    assert tris.check_vittoria()


def test_shouldRecognizeDraw(simple_setup):
    tris.cells = make_cells(XX, XX, OO,
                            OO, OO, XX,
                            XX, OO, XX)
    assert tris.check_patta()


def test_whenPlayerWins_shouldEndGame(setup_after_second_turn):
    tris.turno = 1
    tris.cells = make_cells(XX, XX, NN,
                            OO, OO, NN,
                            NN, NN, NN)
    update = MockUpdate.create_from(callback_data="tris:2", user_id=GIOCATORE_UNO, message_id=123)
    Tris.tris_callback(update, context)
    assert 123 not in Tris.active_tris_games


@pytest.mark.parametrize("user_id", (GIOCATORE_UNO, GIOCATORE_DUE, 789))
def test_ifGameEnded_shouldIgnorePresses(simple_setup, user_id):
    # By default, simple_setup initializes Tris.active_tris_games to {}
    update = MockUpdate.create_from(callback_data="tris:7", user_id=user_id, message_id=123)
    tris.cells = expected_cells = make_cells(XX, XX, XX,
                                             OO, OO, NN,
                                             NN, NN, NN)
    Tris.tris_callback(update, context)
    assert tris.cells == expected_cells


def test_whenPlayerWins_shouldSendMessage(setup_after_second_turn):
    tris.turno = 1
    tris.cells = make_cells(XX, XX, NN,
                            OO, OO, NN,
                            NN, NN, NN)
    update = MockUpdate.create_from(callback_data="tris:2",
                                    user_first_name="Test",
                                    user_id=GIOCATORE_UNO, message_id=123)
    Tris.tris_callback(update, context)
    assert len(bot.result) == 1
    assert bot.result[0]['text'] == "Ha vinto Test"


def test_whenDraw_shouldSendMessage(setup_after_second_turn):
    tris.turno = 1
    tris.cells = make_cells(XX, XX, OO,
                            OO, OO, XX,
                            XX, OO, NN)
    update = MockUpdate.create_from(callback_data="tris:8",
                                    user_id=GIOCATORE_UNO, message_id=123)
    Tris.tris_callback(update, context)
    assert len(bot.result) == 1
    assert bot.result[0]['text'] == "Pareggio!"


def test_whenKnownPlayerWins_shouldSendCustomMessage(setup_after_second_turn):
    load_diz_persone()
    USER_ID_FRANK = 143938748
    tris.giocatore_uno = USER_ID_FRANK
    tris.turno = 1
    tris.cells = make_cells(XX, XX, NN,
                            OO, OO, NN,
                            NN, NN, NN)
    update = MockUpdate.create_from(callback_data="tris:2",
                                    user_first_name="Francesco",
                                    user_id=USER_ID_FRANK, message_id=123)
    Tris.tris_callback(update, context)
    assert len(bot.result) == 1
    assert bot.result[0]['text'] == "Ha vinto Serchio"
