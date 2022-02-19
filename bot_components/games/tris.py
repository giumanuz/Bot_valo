import json
import logging

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackQueryHandler, CallbackContext, Dispatcher, ConversationHandler

from bot_components.utils.os_utils import get_absolute_path

text = '🟢'


class Tris:
    diz_persone = {}

    def __init__(self):
        self.cells = None
        self.current_player = None
        self.vittoria = False
        self.giocatore_uno = ""
        self.giocatore_due = ""

    @staticmethod
    def get_command_name():
        return "Tris"

    @staticmethod
    def get_command_pattern() -> str:
        return "tris"

    @staticmethod
    def get_response_pattern() -> str:
        return r"\d"

    def handle_command(self, update: Update, context: CallbackContext):
        self.cells = [
            [
                InlineKeyboardButton(text=text, callback_data="0"),
                InlineKeyboardButton(text=text, callback_data="1"),
                InlineKeyboardButton(text=text, callback_data="2")
            ],
            [
                InlineKeyboardButton(text=text, callback_data="3"),
                InlineKeyboardButton(text=text, callback_data="4"),
                InlineKeyboardButton(text=text, callback_data="5")
            ],
            [
                InlineKeyboardButton(text=text, callback_data="6"),
                InlineKeyboardButton(text=text, callback_data="7"),
                InlineKeyboardButton(text=text, callback_data="8")
            ]
        ]

        self.current_player = 0
        self.giocatore_uno = ""
        self.giocatore_due = ""
        ris = context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Ecco il tris",
                                       reply_markup=InlineKeyboardMarkup(self.cells))

        return 0, ris

    def check_patta(self):
        for i in range(3):
            for j in range(3):
                if self.cells[i][j].text == text:
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
        return self.cells[row][col].text == text

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

    def handle_response_two(self, update: Update, context: CallbackContext):
        update.callback_query.answer()
        if self.cells is None:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Nessun tris iniziato, usare il comando "tris"'
            )
            return ConversationHandler.END

        if self.giocatore_due == "" and update.callback_query.from_user.id != self.giocatore_uno:
            self.giocatore_due = update.callback_query.from_user.id
        elif self.giocatore_due != update.callback_query.from_user.id:
            return 1

        var = self.gioco_tris(update, context)
        if var != ConversationHandler.END:
            return not var
        return var

    def handle_response(self, update: Update, context: CallbackContext):
        update.callback_query.answer()
        if self.cells is None:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Nessun tris iniziato, usare il comando "tris"'
            )
            return ConversationHandler.END

        if self.giocatore_uno == "":
            self.giocatore_uno = update.callback_query.from_user.id
        elif self.giocatore_uno != update.callback_query.from_user.id:
            return 0

        var = self.gioco_tris(update, context)
        if var != ConversationHandler.END:
            return var
        return var

    def gioco_tris(self, update: Update, context: CallbackContext):
        update.callback_query.answer()
        numero = int(update.callback_query.data)
        if numero == -1 or numero == -2:
            return 0
        riga = numero // 3
        colonna = numero % 3
        if self.current_player:
            self.cells[riga][colonna] = InlineKeyboardButton(
                text="⭕", callback_data="-1")
        else:
            self.cells[riga][colonna] = InlineKeyboardButton(
                text="❌", callback_data="-2")
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


def handle_command(update: Update, context: CallbackContext):
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


def load_diz_persone():
    try:
        with open(get_absolute_path("/resources/text_files/id_persone.json"), "r") as file:
            Tris.diz_persone = json.load(file)
    except OSError as e:
        logging.warning(f"Errore nell'apertura di 'id_persone.json': {e}")


def init_tris(dispatcher: Dispatcher):
    dispatcher.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(
            handle_command, pattern="tris", run_async=True)],
        states={
            0: [CallbackQueryHandler(
                handle_response, pattern=r"\d")],
            1: [CallbackQueryHandler(
                handle_response_two, pattern=r"\d")]
        },
        fallbacks=[],
        conversation_timeout=20,
        per_chat=True,
        per_user=False,
        per_message=False
    ))

