from telegram import Update, InlineKeyboardMarkup
from telegram.ext import Dispatcher

from bot_components.foto import Foto
from bot_components.settings.menu_setting import MenuSetting
from utils.lib_utils import FlowMatrix


class PhotoRemovalSetting(MenuSetting):
    PHOTO_WILL_NOT_BE_DELETED = "Le foto non verranno eliminate... contento te 🤷"
    PHOTO_WILL_BE_DELETED_AFTER = "Le foto verranno eliminate dopo {}"
    TIMER_CHANGE_ERROR = "C'è stato un errore nella modifica del timer😥 Riprova più tardi😅"

    presets = {
        2: "2s", 5: "5s", 10: "10s",
        30: "30s", 60: "1min", 300: "5min",
        1800: "30min", 3600: "1h", Foto.SECONDS_INFINITE: "Mai"
    }
    __MATRIX_ROW_LENGTH = 3

    @property
    def name(self):
        return "Eliminazione foto ⌛"

    @property
    def id(self):
        return "photo-removal-setting"

    def __init__(self, dispatcher: Dispatcher):
        super().__init__(dispatcher)
        self.preset_matrix: InlineKeyboardMarkup = None
        self.add_callback_query_handler(self._preset_click, r"\d+")
        self._init_preset_matrix()

    def _init_preset_matrix(self):
        matrix = FlowMatrix(row_length=self.__MATRIX_ROW_LENGTH)
        for seconds, name in self.presets.items():
            button = self.new_button(name, seconds)
            matrix.append(button)
        self.preset_matrix = InlineKeyboardMarkup(matrix.list)

    def callback(self, update: Update, _):
        update.effective_message.edit_text(
            "Elimina automaticamente le foto inviate dal bot dopo:",
            reply_markup=self.preset_matrix
        )

    def _preset_click(self, update: Update, _):
        message = update.effective_message
        callback_data = update.callback_query.data
        seconds = int(callback_data.split('-')[-1])
        text = ''
        try:
            Foto.set_chat_removal_timer(update.effective_chat, seconds)
            if seconds == Foto.SECONDS_INFINITE:
                text = self.PHOTO_WILL_NOT_BE_DELETED
            else:
                text = self.PHOTO_WILL_BE_DELETED_AFTER.format(self.presets[seconds])
        except AttributeError:
            text = self.TIMER_CHANGE_ERROR
        finally:
            message.edit_text(text)
