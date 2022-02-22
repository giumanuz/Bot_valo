import pytest

from bot_components.games.tris import *
from tests.framework.mockbot import MockBot
from tests.framework.mockcontext import MockContext
from tests.framework.mockdispatcher import MockDispatcher
from tests.framework.mockupdate import MockUpdate

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
    bot.reset_data()
    global tris
    tris = Tris()
    Tris.active_tris_games = {}


@pytest.fixture
def setup_first_turn_with_x_in_upperleft_corner():
    bot.reset_data()
    global tris
    tris = Tris()
    Tris.active_tris_games = {123: tris}
    tris.cells = make_cells(XX, NN, NN,
                            NN, NN, NN,
                            NN, NN, NN)
    tris.giocatore_uno = GIOCATORE_UNO
    tris.turno = 2


def test_isTrisShown(simple_setup):
    update = MockUpdate.from_message("")
    Tris.show_tris(update, context)
    res = bot.result
    assert len(res) == 1
    assert 'reply_markup' in res[0]
    assert is_empty_tris(res[0]['reply_markup'])


def test_ifFirstUserPresses_putsAnX(simple_setup):
    Tris.active_tris_games = {123: tris}
    update = MockUpdate.create_from(message_id=123, callback_data="tris:0")
    Tris.tris_callback(update, context)
    expected_cells = make_cells(XX, NN, NN,
                                NN, NN, NN,
                                NN, NN, NN)
    assert are_cells_equal(expected_cells, tris.cells)


def test_ifUserPresses_editsMessageMarkup(simple_setup):
    Tris.active_tris_games = {123: tris}
    update = MockUpdate.create_from(message_id=123, callback_data="tris:0")
    Tris.tris_callback(update, context)
    assert update.effective_message.reply_markup.inline_keyboard[0][0].text == XX


def test_ifSameUserPressesOtherCell_putsAnO(setup_first_turn_with_x_in_upperleft_corner):
    update = MockUpdate.create_from(callback_data="tris:3", user_id=GIOCATORE_UNO, message_id=123)
    Tris.tris_callback(update, context)
    expected_cells = make_cells(XX, NN, NN,
                                OO, NN, NN,
                                NN, NN, NN)
    assert are_cells_equal(expected_cells, tris.cells)


def test_ifOtherUserPressesOtherCell_putsAnO(setup_first_turn_with_x_in_upperleft_corner):
    update = MockUpdate.create_from(callback_data="tris:3", user_id=GIOCATORE_DUE, message_id=123)
    Tris.tris_callback(update, context)
    expected_cells = make_cells(XX, NN, NN,
                                OO, NN, NN,
                                NN, NN, NN)
    assert are_cells_equal(expected_cells, tris.cells)


def is_empty_tris(markup: InlineKeyboardMarkup) -> bool:
    cells = markup.inline_keyboard
    return all(cells[i][j].text == Tris.EMPTY_CELL
               for i in range(3) for j in range(3))


def make_cells(ul, uc, ur,
               cl, cc, cr,
               dl, dc, dr) -> InlineKeyboardMarkup:
    return [[
        InlineKeyboardButton(text=ul, callback_data="tris:0"),
        InlineKeyboardButton(text=uc, callback_data="tris:1"),
        InlineKeyboardButton(text=ur, callback_data="tris:2")
    ],
        [
            InlineKeyboardButton(text=cl, callback_data="tris:3"),
            InlineKeyboardButton(text=cc, callback_data="tris:4"),
            InlineKeyboardButton(text=cr, callback_data="tris:5")
        ],
        [
            InlineKeyboardButton(text=dl, callback_data="tris:6"),
            InlineKeyboardButton(text=dc, callback_data="tris:7"),
            InlineKeyboardButton(text=dr, callback_data="tris:8")
        ]]


def are_cells_equal(first, second) -> bool:
    return all(first[i][j].text == second[i][j].text
               for i in range(3) for j in range(3))
