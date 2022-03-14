from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CommandHandler, Dispatcher

from utils.lib_utils import FlowMatrix


class Menu:
    __BUTTONS_PER_ROW = 2
    __MENU_TEXT = "〰〰〰〰 MENU 〰〰〰〰"

    buttons_matrix = FlowMatrix(row_length=__BUTTONS_PER_ROW)

    @classmethod
    def init(cls, dispatcher: Dispatcher):
        dispatcher.add_handler(CommandHandler("menu", Menu.show, run_async=True))

    @classmethod
    def show(cls, update: Update, _=None):
        buttons_markup = InlineKeyboardMarkup(cls.buttons_matrix.list)
        update.effective_chat.send_message(cls.__MENU_TEXT, reply_markup=buttons_markup)

    @classmethod
    def register_button(cls, name: str, callback: str):
        new_button = InlineKeyboardButton(name, callback_data=callback)
        cls.buttons_matrix.append(new_button)
