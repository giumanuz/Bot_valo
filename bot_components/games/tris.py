import json
import logging

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackQueryHandler, CallbackContext, Dispatcher

from bot_components.utils.os_utils import get_absolute_path


def init_tris(dispatcher: Dispatcher):
    load_diz_persone()
    dispatcher.add_handler(CallbackQueryHandler(
        Tris.show_tris, pattern="^tris-callback$", run_async=True))
    dispatcher.add_handler(CallbackQueryHandler(
        Tris.tris_callback, pattern=r"tris:[0-9]", run_async=True
    ))


def load_diz_persone():
    try:
        with open(get_absolute_path("/resources/text_files/id_persone.json"), "r") as file:
            Tris.diz_persone = json.load(file)
            print(Tris.diz_persone)
    except OSError as e:
        logging.warning(f"Errore nell'apertura di 'id_persone.json': {e}")


def get_coordinate(update):
    numero = int(update.callback_query.data[5:])
    riga = numero // 3
    colonna = numero % 3
    return riga, colonna


class Tris:
    active_tris_games = {}
    diz_persone = {}

    EMPTY_CELL = '🟢'
    X_CELL = '❌'
    O_CELL = '⭕'

    def __init__(self):
        self.giocatore_corrente = None
        self.partita_attiva = True
        self.giocatore_uno: int = -1
        self.giocatore_due: int = -1
        self.message_id: int = -1
        self.cells = [
            [
                InlineKeyboardButton(text=self.EMPTY_CELL, callback_data="tris:0"),
                InlineKeyboardButton(text=self.EMPTY_CELL, callback_data="tris:1"),
                InlineKeyboardButton(text=self.EMPTY_CELL, callback_data="tris:2")
            ],
            [
                InlineKeyboardButton(text=self.EMPTY_CELL, callback_data="tris:3"),
                InlineKeyboardButton(text=self.EMPTY_CELL, callback_data="tris:4"),
                InlineKeyboardButton(text=self.EMPTY_CELL, callback_data="tris:5")
            ],
            [
                InlineKeyboardButton(text=self.EMPTY_CELL, callback_data="tris:6"),
                InlineKeyboardButton(text=self.EMPTY_CELL, callback_data="tris:7"),
                InlineKeyboardButton(text=self.EMPTY_CELL, callback_data="tris:8")
            ]
        ]

    def check_patta(self):
        for i in range(3):
            for j in range(3):
                if self.cells[i][j].text == self.EMPTY_CELL:
                    return False
        return True

    def check_vittoria(self):
        for i in range(3):
            if self.check_row(i) or self.check_column(i):
                return True
        return self.check_diagonals()

    def check_row(self, i):
        return (self.cells[i][0].text == self.cells[i][1].text == self.cells[i][2].text
                and not self.is_cell_empty(i, 0))

    def check_column(self, i):
        return (self.cells[0][i].text == self.cells[1][i].text == self.cells[2][i].text
                and not self.is_cell_empty(2, i))

    def check_diagonals(self):
        tris_on_main_diagonal = (self.cells[0][0].text == self.cells[1][1].text == self.cells[2][2].text
                                 and not self.is_cell_empty(2, 2))
        tris_on_minor_diagonal = (self.cells[0][2].text == self.cells[1][1].text == self.cells[2][0].text
                                  and not self.is_cell_empty(2, 0))
        return tris_on_minor_diagonal or tris_on_main_diagonal

    def is_cell_empty(self, row, col):
        return self.cells[row][col].text == self.EMPTY_CELL

    def make_move(self, update: Update):
        simbolo = self.X_CELL if self.giocatore_corrente == self.giocatore_uno else self.O_CELL
        self.cambia_giocatore()
        riga, colonna = get_coordinate(update)
        if self.cells[riga][colonna].text == self.EMPTY_CELL:
            self.cells[riga][colonna].text = simbolo

    def cambia_giocatore(self):
        if self.giocatore_corrente == self.giocatore_uno:
            self.giocatore_corrente = self.giocatore_due
        else:
            self.giocatore_corrente = self.giocatore_uno

    def end_game(self):
        self.partita_attiva = False
        Tris.active_tris_games.pop(self.message_id)

    @classmethod
    def show_tris(cls, update: Update, context: CallbackContext):
        tris = Tris()
        message = context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Ecco il tris",
                                           reply_markup=InlineKeyboardMarkup(tris.cells))
        tris.message_id = message.message_id
        cls.active_tris_games[message.message_id] = tris

    @classmethod
    def tris_callback(cls, update: Update, context: CallbackContext):
        update.callback_query.answer()

        message_id = update.effective_message.message_id
        tris: Tris = cls.active_tris_games.get(message_id, None)
        if tris is None or not tris.partita_attiva:
            return

        user_id = update.effective_user.id
        if tris.giocatore_uno == -1:
            tris.giocatore_uno = tris.giocatore_corrente = user_id
        elif tris.giocatore_due == -1:
            tris.giocatore_due = tris.giocatore_corrente = user_id

        if tris.giocatore_corrente == user_id:
            tris.make_move(update)
            update.effective_message.edit_reply_markup(InlineKeyboardMarkup(tris.cells))
            if tris.check_vittoria():
                id_giocatore = str(tris.giocatore_uno if tris.giocatore_corrente == tris.giocatore_due else tris.giocatore_due)
                nome_giocatore = Tris.diz_persone.get(id_giocatore, update.effective_user.first_name)
                context.bot.send_message(update.effective_chat.id, f"Ha vinto {nome_giocatore}")
                tris.end_game()
            elif tris.check_patta():
                context.bot.send_message(update.effective_chat.id, "Pareggio!")
                tris.end_game()
