import json
import os

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CallbackQueryHandler, CallbackContext, Dispatcher, ConversationHandler


class Tris:
    def __init__(self):
        self.__cells = None
        self.__current_player = None
        self.__vittoria = False
        self.__giocatore_uno = ""
        self.__giocatore_due = ""
        self.diz_persone = {}
        try:
            with open("./bot_components/commands/id_persone.json", "r") as file:
                self.diz_persone = json.load(file)
        except Exception as e:
            print(e)

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
        self.__cells = [
            [
                InlineKeyboardButton(text="🟢️", callback_data="0"),
                InlineKeyboardButton(text="🟢", callback_data="1"),
                InlineKeyboardButton(text="🟢", callback_data="2")
            ],
            [
                InlineKeyboardButton(text="🟢", callback_data="3"),
                InlineKeyboardButton(text="🟢", callback_data="4"),
                InlineKeyboardButton(text="🟢", callback_data="5")
            ],
            [
                InlineKeyboardButton(text="🟢", callback_data="6"),
                InlineKeyboardButton(text="🟢", callback_data="7"),
                InlineKeyboardButton(text="🟢", callback_data="8")
            ]
        ]

        self.__current_player = 0
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Ecco il tris",
                                 reply_markup=InlineKeyboardMarkup(self.__cells))

        return 0

    def __check_tris(self):
        for i in range(3):
            if self.__check_row(i) or self.__check_column(i):
                return True
        if self.__check_main_diagonal() or self.__check_minor_diagonal():
            return True
        return False

    def __is_cell_empty(self, row, col):
        return self.__cells[row][col].text == '🟢'

    def __check_minor_diagonal(self):
        return (self.__cells[0][2].text == self.__cells[1][1].text == self.__cells[2][0].text
                and not self.__is_cell_empty(2, 0))

    def __check_main_diagonal(self):
        return (self.__cells[0][0].text == self.__cells[1][1].text == self.__cells[2][2].text
                and not self.__is_cell_empty(2, 2))

    def __check_column(self, i):
        return (self.__cells[0][i].text == self.__cells[1][i].text == self.__cells[2][i].text
                and not self.__is_cell_empty(2, i))

    def __check_row(self, i):
        return (self.__cells[i][0].text == self.__cells[i][1].text == self.__cells[i][2].text
                and not self.__is_cell_empty(i, 0))

    def handle_response_two(self, update: Update, context: CallbackContext):
        update.callback_query.answer()
        if self.__cells is None:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Nessun tris iniziato, usare il comando "tris"'
            )
            return ConversationHandler.END

        if self.__giocatore_due == "" and update.callback_query.from_user.id != self.__giocatore_uno:
            self.__giocatore_due = update.callback_query.from_user.id
        elif self.__giocatore_due != update.callback_query.from_user.id:
            return 1

        var = self.gioco_tris(update, context)
        if var != ConversationHandler.END:
            return not var
        return var

    def handle_response(self, update: Update, context: CallbackContext):
        update.callback_query.answer()
        if self.__cells is None:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Nessun tris iniziato, usare il comando "tris"'
            )
            return ConversationHandler.END

        if self.__giocatore_uno == "":
            self.__giocatore_uno = update.callback_query.from_user.id
        elif self.__giocatore_uno != update.callback_query.from_user.id:
            return 0

        var = self.gioco_tris(update, context)
        if var != ConversationHandler.END:
            return var
        return var

    def gioco_tris(self, update: Update, context: CallbackContext):
        update.callback_query.answer()
        numero = int(update.callback_query.data)
        if numero == -1 or numero == -2 or self.__vittoria == True:
            return 0
        riga = numero // 3
        colonna = numero % 3
        if self.__current_player:
            self.__cells[riga][colonna] = InlineKeyboardButton(
                text="⭕", callback_data="-1")
        else:
            self.__cells[riga][colonna] = InlineKeyboardButton(
                text="❌", callback_data="-2")
        self.__current_player = not self.__current_player
        update.callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(self.__cells))
        if self.__check_tris():
            if self.__current_player:
                if str(self.__giocatore_uno) not in self.diz_persone:
                    nome_giocatore = update.callback_query.from_user.first_name
                else:
                    nome_giocatore = self.diz_persone[str(self.__giocatore_uno)]
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f'Ha vinto {nome_giocatore}'
                )
            else:
                if str(self.__giocatore_due) not in self.diz_persone:
                    nome_giocatore = update.callback_query.from_user.first_name
                else:
                    nome_giocatore = self.diz_persone[str(self.__giocatore_due)]
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f'Ha vinto {nome_giocatore}'
                )

            self.__vittoria = True
            return ConversationHandler.END
        return 1


def init_tris(dispatcher: Dispatcher):
    tris = Tris()
    dispatcher.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(
            tris.handle_command, pattern=tris.get_command_pattern(), run_async=True)],
        states={
            0: [CallbackQueryHandler(
                tris.handle_response, pattern=tris.get_response_pattern())],
            1: [CallbackQueryHandler(
                tris.handle_response_two, pattern=tris.get_response_pattern())]
        },
        fallbacks=[],
        per_chat=True,
        per_user=False,
        per_message=False
    ))
