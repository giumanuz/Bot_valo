from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext, Dispatcher


class Tris:

    def __init__(self) -> None:
        self.__array_list = None
        self.__corrent_player = None
        pass

    @staticmethod
    def get_command_name():
        return "Tris"

    @staticmethod
    def get_command_pattern() -> None:
        return "tris"

    @staticmethod
    def get_response_pattern() -> None:
        return "\d"

    def command_handler(self, update: Update, context: CallbackContext) -> None:
        self.__array_list = [[InlineKeyboardButton(text="🟢️", callback_data="0"),
                              InlineKeyboardButton(
                                  text="🟢", callback_data="1"),
                              InlineKeyboardButton(text="🟢", callback_data="2")],
                             [InlineKeyboardButton(text="🟢", callback_data="3"),
                              InlineKeyboardButton(
                                  text="🟢", callback_data="4"),
                              InlineKeyboardButton(text="🟢", callback_data="5")],
                             [InlineKeyboardButton(text="🟢", callback_data="6"),
                              InlineKeyboardButton(
                                  text="🟢", callback_data="7"),
                              InlineKeyboardButton(text="🟢", callback_data="8")]]

        self.__corrent_player = 0

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Ecco il tris",
                                 reply_markup=InlineKeyboardMarkup(self.__array_list))
        pass

    def __check(self, update: Update, context: CallbackContext):
        for i in range(3):
            if (self.__array_list[i][0].text == self.__array_list[i][1].text == self.__array_list[i][2].text and
                self.__array_list[i][0].text != '🟢') or (
                    self.__array_list[0][i].text == self.__array_list[1][i].text == self.__array_list[2][i].text and
                    self.__array_list[2][i].text != '🟢'):
                return True
        if (self.__array_list[0][0].text == self.__array_list[1][1].text == self.__array_list[2][2].text and
            self.__array_list[2][2].text != '🟢') or (
                self.__array_list[0][2].text == self.__array_list[1][1].text == self.__array_list[2][0].text and
                self.__array_list[2][0].text != '🟢'):
            return True
        return False

    def response_handler(self, update: Update, context: CallbackContext) -> None:

        if self.__array_list == None:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='Nessun tris iniziato, usare il comando "tris"')
            return

        update.callback_query.answer()
        numero = int(update.callback_query.data)
        if numero == -1 or numero == -2:
            return
        riga = numero // 3
        colonna = numero % 3
        if self.__corrent_player:
            self.__array_list[riga][colonna] = InlineKeyboardButton(
                text="⭕", callback_data="-1")
        else:
            self.__array_list[riga][colonna] = InlineKeyboardButton(
                text="❌", callback_data="-2")
        self.__corrent_player = not self.__corrent_player
        update.callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(self.__array_list))
        if self.__check(update, context):
            if self.__corrent_player:
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text='Ha vinto ❌')
            else:
                context.bot.send_message(
                    chat_id=update.effective_chat.id, text='Ha vinto ⭕')
        pass

    pass


def init_tris(dispatcher: Dispatcher) -> None:
    tris = Tris()
    dispatcher.add_handler(CallbackQueryHandler(
        tris.command_handler, pattern=tris.get_command_pattern(), run_async=True))
    dispatcher.add_handler(CallbackQueryHandler(
        tris.response_handler, pattern=tris.get_response_pattern()))
    pass
