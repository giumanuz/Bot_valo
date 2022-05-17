from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from bot_components.games.tris import Tris


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
