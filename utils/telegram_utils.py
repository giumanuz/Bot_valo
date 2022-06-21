from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from utils.lib_utils import FlowMatrix


def get_effective_text(update):
    """Restituisce il testo effettivo del messaggio
    contenuto in `update`."""
    if update.effective_message.caption is not None:
        return str(update.effective_message.caption).lower()
    elif update.effective_message.text is not None:
        return str(update.effective_message.text).lower()


class ButtonFlowMatrix:
    def __init__(self, row_length: int):
        self.__flowmatrix = FlowMatrix(row_length)

    def append(self, button_text: str, callback_data: object):
        self.__flowmatrix.append(InlineKeyboardButton(button_text, callback_data=callback_data))

    @property
    def keyboard_markup(self):
        return InlineKeyboardMarkup(self.__flowmatrix.list)
