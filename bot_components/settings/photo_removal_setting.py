from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CallbackQueryHandler

from bot_components.foto import Foto
from bot_components.settings.menu_setting import MenuSetting
from utils.lib_utils import FlowMatrix


class PhotoRemovalSetting(MenuSetting):
    name = "Timer foto"
    id = "photo-removal-setting"

    presets = {
        2: "2s", 5: "5s", 10: "10s",
        30: "30s", 60: "1min", 300: "5min",
        1800: "30min", 3600: "1h", Foto.SECONDS_INFINITE: "Mai"
    }
    preset_matrix: list[list[InlineKeyboardButton]] = []

    @classmethod
    def init(cls, dispatcher: Dispatcher):
        matrix = FlowMatrix(row_length=3)
        dispatcher.add_handler(CallbackQueryHandler(
            cls._preset_click,
            pattern=fr"^{cls.name}-\d+"
        ))
        for seconds, name in cls.presets.items():
            button = InlineKeyboardButton(
                name,
                callback_data=f"{cls.name}-{seconds}"
            )
            matrix.append(button)
        cls.preset_matrix = InlineKeyboardMarkup(matrix.list)

    @classmethod
    def callback(cls, update: Update, _):
        update.effective_message.edit_text(
            "🔧 Imposta preset 🔧",
            reply_markup=cls.preset_matrix
        )

    @classmethod
    def _preset_click(cls, update: Update, _):
        callback_data = update.callback_query.data
        seconds = int(callback_data.split('-')[-1])
        try:
            Foto.set_chat_removal_timer(update.effective_chat, seconds)
            if seconds == Foto.SECONDS_INFINITE:
                update.effective_message.edit_text("Le foto non verranno eliminate.")
            else:
                update.effective_message.edit_text(f"Le foto verranno eliminate dopo {cls.presets[seconds]}.")
        except AttributeError:
            update.effective_message.edit_text("C'è stato un errore nella modifica del timer. "
                                               "Riprova più tardi")
