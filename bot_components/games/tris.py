from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackQueryHandler, CallbackContext, Dispatcher

from utils.db_utils import get_json_data


def init_tris(dispatcher: Dispatcher):
    load_diz_persone()
    dispatcher.add_handler(CallbackQueryHandler(Tris.show_tris, pattern=r"tris-callback", run_async=True))
    dispatcher.add_handler(CallbackQueryHandler(Tris.tris_callback, pattern=r"tris:[0-9]", run_async=True))


def load_diz_persone():
    Tris.diz_persone = get_json_data("configs/id_persone.json")


def get_coordinate(update: Update):
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
            return
        elif tris.check_patta():
            context.bot.send_message(chat_id, "Pareggio!")
            Tris.active_tris_games.pop(tris.message_id)
            return
        tris.cambia_giocatore()

    @classmethod
    def show_tris(cls, update: Update, context: CallbackContext):
        tris = Tris()
        message = context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Ecco il tris",
                                           reply_markup=InlineKeyboardMarkup(tris.cells))
        tris.message_id = message.message_id
        cls.active_tris_games[message.message_id] = tris

    def __init__(self):
        self.giocatore_uno = None
        self.giocatore_due = None
        self.message_id = None
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

    @property
    def giocatore_corrente(self):
        return self.giocatore_uno if self.turno == 1 else self.giocatore_due

    def is_cell_empty(self, row, col):
        return self.cells[row][col].text == self.EMPTY_CELL

    def user_init_required(self):
        return self.giocatore_uno is None or self.giocatore_due is None

    def initialize_user(self, user_id):
        if self.giocatore_uno is None:
            self.giocatore_uno = user_id
        elif self.giocatore_due is None:
            self.giocatore_due = user_id

    def make_move_and_edit_message(self, update: Update):
        riga, colonna = get_coordinate(update)
        self.cells[riga][colonna].text = self.get_current_cell_type()
        update.effective_message.edit_reply_markup(InlineKeyboardMarkup(self.cells))

    def get_current_cell_type(self) -> str:
        return Tris.X_CELL if self.turno == 1 else Tris.O_CELL

    def cambia_giocatore(self):
        self.turno = 2 if self.turno == 1 else 1

    def check_patta(self) -> bool:
        return all(self.cells[i][j].text != self.EMPTY_CELL
                   for i in range(3) for j in range(3))

    def check_vittoria(self) -> bool:
        for i in range(3):
            if self.check_row(i) or self.check_column(i):
                return True
        return self.check_diagonals()

    def check_row(self, i) -> bool:
        return (self.cells[i][0].text == self.cells[i][1].text == self.cells[i][2].text
                and not self.is_cell_empty(i, 0))

    def check_column(self, i) -> bool:
        return (self.cells[0][i].text == self.cells[1][i].text == self.cells[2][i].text
                and not self.is_cell_empty(2, i))

    def check_diagonals(self) -> bool:
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
        return self.diz_persone.get(str(id_vincitore), update.effective_user.first_name)
