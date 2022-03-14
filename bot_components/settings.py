import math

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CallbackQueryHandler

from bot_components.menu import Menu
from utils.lib_utils import FlowMatrix


class ChatSettings:
    __BUTTONS_PER_ROW = 2
    settings_matrix = FlowMatrix(row_length=__BUTTONS_PER_ROW)

    @classmethod
    def init(cls, dispatcher: Dispatcher):
        dispatcher.add_handler(CallbackQueryHandler(
            cls.show_settings,
            pattern="^chat-settings$",
            run_async=True
        ))
        Menu.register_button("Impostazioni", "chat-settings")

    @classmethod
    def __add_setting(cls, name: str, callback, dispatcher: Dispatcher):
        setting_button = InlineKeyboardButton(name, callback_data=callback)
        cls.settings_matrix.append(setting_button)
        dispatcher.add_handler(CallbackQueryHandler(
            callback,
            pattern=f"^{'-'.join(name.lower().split())}$"
        ))

    @classmethod
    def show_settings(cls, update: Update, _=None):
        mes = update.effective_message
        settings_markup = InlineKeyboardMarkup(cls.settings_matrix.list)
        mes.edit_text("Impostazioni")
        mes.edit_reply_markup(settings_markup)

    __PHOTO_REMOVAL_PRESETS = FlowMatrix.from_list(
        [2, 5, 10, 20, 30, 60, 120, math.inf],
        row_length=2
    )

    @classmethod
    def s_photo_removal_timer(cls, update: Update, _=None):
        pass
