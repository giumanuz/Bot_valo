import json
import logging

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackQueryHandler, CallbackContext, Dispatcher, ConversationHandler

from bot_components.utils.os_utils import get_absolute_path


class Tris:
    EMPTY_CELL = '🟢'

    diz_persone = {}

    def __init__(self):
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
        self.current_player = 0
        self.vittoria = False
        self.giocatore_uno = ""
        self.giocatore_due = ""

    # region controlli
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
        if self.check_main_diagonal() or self.check_minor_diagonal():
            return True
        return False

    def is_cell_empty(self, row, col):
        return self.cells[row][col].text == self.EMPTY_CELL

    def check_minor_diagonal(self):
        return (self.cells[0][2].text == self.cells[1][1].text == self.cells[2][0].text
                and not self.is_cell_empty(2, 0))

    def check_main_diagonal(self):
        return (self.cells[0][0].text == self.cells[1][1].text == self.cells[2][2].text
                and not self.is_cell_empty(2, 2))

    def check_column(self, i):
        return (self.cells[0][i].text == self.cells[1][i].text == self.cells[2][i].text
                and not self.is_cell_empty(2, i))

    def check_row(self, i):
        return (self.cells[i][0].text == self.cells[i][1].text == self.cells[i][2].text
                and not self.is_cell_empty(i, 0))

    # endregion

    def handle_response_two(self, update: Update, context: CallbackContext):
        update.callback_query.answer()
        if self.cells is None:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Nessun tris iniziato, usare il comando "tris"'
            )
            return  # ConversationHandler.END

        if self.giocatore_due == "" and update.callback_query.from_user.id != self.giocatore_uno:
            self.giocatore_due = update.callback_query.from_user.id
        elif self.giocatore_due != update.callback_query.from_user.id:
            return

        self.gioco_tris(update, context)

    def handle_response(self, update: Update, context: CallbackContext):
        update.callback_query.answer()
        if self.cells is None:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Nessun tris iniziato, usare il comando "tris"'
            )
            return  # ConversationHandler.END

        if self.giocatore_uno == "":
            self.giocatore_uno = update.callback_query.from_user.id
        elif self.giocatore_uno != update.callback_query.from_user.id:
            return
        self.gioco_tris(update, context)

    def gioco_tris(self, update: Update, context: CallbackContext):
        if update.callback_query.data is None:
            return
        update.callback_query.answer()
        numero = int(update.callback_query.data[5:])
        riga = numero // 3
        colonna = numero % 3
        if self.current_player:
            self.cells[riga][colonna] = InlineKeyboardButton(text="⭕")
        else:
            self.cells[riga][colonna] = InlineKeyboardButton(text="❌")
        self.current_player = not self.current_player
        update.callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(self.cells))
        if self.check_vittoria():
            if self.current_player:
                if str(self.giocatore_uno) not in self.diz_persone:
                    nome_giocatore = update.callback_query.from_user.first_name
                else:
                    nome_giocatore = self.diz_persone[str(self.giocatore_uno)]
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f'Ha vinto {nome_giocatore}'
                )
            else:
                if str(self.giocatore_due) not in self.diz_persone:
                    nome_giocatore = update.callback_query.from_user.first_name
                else:
                    nome_giocatore = self.diz_persone[str(self.giocatore_due)]
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f'Ha vinto {nome_giocatore}'
                )
            return ConversationHandler.END
        elif self.check_patta():
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'Partita pareggiata'
            )
            return ConversationHandler.END
        return 1


dict_tris = {}


def show_tris(update: Update, context: CallbackContext):
    tris = Tris()
    (ris, message) = tris.handle_command(update, context)
    dict_tris[message.message_id] = tris
    return ris


def handle_response(update: Update, context: CallbackContext):
    mess = update.callback_query.message.message_id
    tris = dict_tris[mess]
    ris = tris.handle_response(update, context)
    if ris == ConversationHandler.END:
        dict_tris.pop(mess)
    return ris


def handle_response_two(update: Update, context: CallbackContext):
    mess = update.callback_query.message.message_id
    tris = dict_tris[mess]
    ris = tris.handle_response_two(update, context)
    if ris == ConversationHandler.END:
        dict_tris.pop(mess)
    return ris


def tris_callback(update: Update, context: CallbackContext):
    update.callback_query.answer()
    tris = dict_tris[update.effective_message.message_id]
    tris.handle_response(update, context)
    tris.handle_response_two(update, context)


def load_diz_persone():
    try:
        with open(get_absolute_path("/resources/text_files/id_persone.json"), "r") as file:
            Tris.diz_persone = json.load(file)
    except OSError as e:
        logging.warning(f"Errore nell'apertura di 'id_persone.json': {e}")


def init_tris(dispatcher: Dispatcher):
    dispatcher.add_handler(CallbackQueryHandler(
        show_tris, pattern="tris_callback", run_async=True))
    dispatcher.add_handler(CallbackQueryHandler(
        tris_callback, pattern=r"tris:-?\d", run_async=True
    ))
