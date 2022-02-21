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

    @classmethod
    def tris_callback(cls, update: Update, context: CallbackContext):
        update.callback_query.answer()

        message_id = update.effective_message.message_id
        tris: Tris = cls.active_tris_games.get(message_id, None)
        if tris is None or not tris.is_cell_empty(*get_coordinate(update)):
            return

        user_id = update.effective_user.id
        if tris.user_init_required():
            tris.initialize_user(user_id)

        chat_id = update.effective_chat.id
        if tris.giocatore_corrente != user_id:
            return
        tris.make_move_and_edit_message(update)
        if tris.check_vittoria():
            vincitore = tris.get_nome_vincitore(update)
            context.bot.send_message(chat_id, f"Ha vinto {vincitore}")
            Tris.active_tris_games.pop(tris.message_id)
        elif tris.check_patta():
            context.bot.send_message(chat_id, "Pareggio!")
            Tris.active_tris_games.pop(tris.message_id)

    @classmethod
    def show_tris(cls, update: Update, context: CallbackContext):
        tris = Tris()
        message = context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Ecco il tris",
                                           reply_markup=InlineKeyboardMarkup(tris.cells))
        tris.message_id = message.message_id
        cls.active_tris_games[message.message_id] = tris

    def __init__(self):
        self.giocatore_corrente = None
        self.giocatore_uno = -1
        self.giocatore_due = -1
        self.message_id = -1
        self.turno = 1
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

    def is_cell_empty(self, row, col):
        return self.cells[row][col].text == self.EMPTY_CELL

    def user_init_required(self):
        return self.giocatore_uno == -1 or self.giocatore_due == -1

    def initialize_user(self, user_id):
        if self.giocatore_uno == -1:
            self.giocatore_uno = self.giocatore_corrente = user_id
        elif self.giocatore_due == -1:
            self.giocatore_due = self.giocatore_corrente = user_id

    def make_move_and_edit_message(self, update: Update):
        simbolo = self.imposta_simbolo()
        self.cambia_giocatore()
        riga, colonna = get_coordinate(update)
        self.cells[riga][colonna].text = simbolo
        update.effective_message.edit_reply_markup(InlineKeyboardMarkup(self.cells))

    def imposta_simbolo(self) -> str:
        if self.turno == 1:
            return Tris.X_CELL
        elif self.turno == 2:
            return Tris.O_CELL
        else:
            raise Exception("Turno non valido")

    def cambia_giocatore(self):
        if self.turno == 1:
            self.giocatore_corrente = self.giocatore_due
            self.turno = 2
        elif self.turno == 2:
            self.giocatore_corrente = self.giocatore_uno
            self.turno = 1
        else:
            raise Exception("Turno non valido")

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

    def get_nome_vincitore(self, update: Update) -> str:
        if self.giocatore_corrente == self.giocatore_uno:
            id_vincitore = self.giocatore_uno
        else:
            id_vincitore = self.giocatore_due
        return self.diz_persone.get(id_vincitore, update.effective_user.first_name)
