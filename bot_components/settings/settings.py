from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CallbackQueryHandler

from bot_components.menu import Menu
from bot_components.settings.photo_removal_setting import PhotoRemovalSetting
from utils.lib_utils import FlowMatrix


class ChatSettings:
    __BUTTONS_PER_ROW = 2
    settings_matrix = FlowMatrix(row_length=__BUTTONS_PER_ROW)
    dispatcher: Dispatcher

    @classmethod
    def init(cls, dispatcher: Dispatcher):
        cls.dispatcher = dispatcher
        dispatcher.add_handler(CallbackQueryHandler(
            cls.show_settings,
            pattern="^chat-settings$",
            run_async=True
        ))
        Menu.register_button("🔧Impostazioni🔧", "chat-settings")
        cls._init_settings()

    @classmethod
    def _init_settings(cls):
        cls.__add_setting(PhotoRemovalSetting)

    @classmethod
    def __add_setting(cls, setting):
        cls.dispatcher.add_handler(CallbackQueryHandler(
            setting.callback,
            pattern=f"^{setting.id}$"
        ))
        setting.register(cls.dispatcher)
        setting_button = InlineKeyboardButton(setting.name, callback_data=setting.id)
        cls.settings_matrix.append(setting_button)

    @classmethod
    def show_settings(cls, update: Update, _=None):
        settings_markup = InlineKeyboardMarkup(cls.settings_matrix.list)
        update.effective_message.edit_text("🔧 Impostazioni 🔧", reply_markup=settings_markup)
