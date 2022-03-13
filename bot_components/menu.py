from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CommandHandler, Dispatcher


class Menu:
    __BUTTONS_PER_ROW = 2
    __MENU_TEXT = "〰〰〰〰 MENU 〰〰〰〰"

    buttons_list: list[list[InlineKeyboardButton]] = []

    @classmethod
    def init(cls, dispatcher: Dispatcher):
        dispatcher.add_handler(CommandHandler("menu", Menu.show, run_async=True))

    @classmethod
    def show(cls, update: Update, _=None):
        buttons_markup = InlineKeyboardMarkup(cls.buttons_list)
        update.effective_chat.send_message(cls.__MENU_TEXT, reply_markup=buttons_markup)

    @classmethod
    def register_button(cls, name: str, callback: str):
        cls._create_cell_if_necessary()
        new_button = InlineKeyboardButton(name, callback_data=callback)
        cls.buttons_list[-1].append(new_button)

    @classmethod
    def _create_cell_if_necessary(cls):
        if len(cls.buttons_list) == 0 or cls._list_is_full():
            cls.buttons_list.append([])

    @classmethod
    def _list_is_full(cls):
        return len(cls.buttons_list[-1]) == cls.__BUTTONS_PER_ROW
