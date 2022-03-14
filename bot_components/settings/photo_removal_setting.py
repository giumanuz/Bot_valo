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
    preset_matrix: list[list[InlineKeyboardButton]] = None
    __MATRIX_ROW_LENGTH = 3

    PHOTO_WILL_NOT_BE_DELETED = "Le foto non verranno eliminate... contento te 🤷"
    PHOTO_WILL_BE_DELETED_AFTER = "Le foto verranno eliminate dopo {}"
    TIMER_CHANGE_ERROR = "C'è stato un errore nella modifica del timer😥 Riprova più tardi😅"

    @classmethod
    def init(cls, dispatcher: Dispatcher):
        matrix = FlowMatrix(row_length=cls.__MATRIX_ROW_LENGTH)
        cls._add_callback_handler(dispatcher)
        cls._init_preset_matrix(matrix)

    @classmethod
    def _init_preset_matrix(cls, matrix):
        for seconds, name in cls.presets.items():
            button = InlineKeyboardButton(
                name,
                callback_data=f"{cls.name}-{seconds}"
            )
            matrix.append(button)
        cls.preset_matrix = InlineKeyboardMarkup(matrix.list)

    @classmethod
    def _add_callback_handler(cls, dispatcher):
        dispatcher.add_handler(CallbackQueryHandler(
            cls._preset_click,
            pattern=fr"^{cls.name}-\d+"
        ))

    @classmethod
    def callback(cls, update: Update, _):
        update.effective_message.edit_text(
            "🔧 Imposta preset 🔧",
            reply_markup=cls.preset_matrix
        )

    @classmethod
    def _preset_click(cls, update: Update, _):
        message = update.effective_message
        callback_data = update.callback_query.data
        seconds = int(callback_data.split('-')[-1])
        text = ''
        try:
            Foto.set_chat_removal_timer(update.effective_chat, seconds)
            if seconds == Foto.SECONDS_INFINITE:
                text = cls.PHOTO_WILL_NOT_BE_DELETED
            else:
                text = cls.PHOTO_WILL_BE_DELETED_AFTER.format(cls.presets[seconds])
        except AttributeError:
            text = cls.TIMER_CHANGE_ERROR
        finally:
            message.edit_text(text)
