from telegram import InlineKeyboardMarkup


class MockMessage:
    def __init__(self, text, message_id=-1, reply_markup: InlineKeyboardMarkup = None):
        self._text = text
        self._message_id = message_id
        self._reply_markup = reply_markup

    @property
    def text(self):
        return self._text

    @property
    def message_id(self):
        return self._message_id

    @property
    def reply_markup(self):
        return self._reply_markup

    def edit_reply_markup(self, reply_markup: InlineKeyboardMarkup):
        self._reply_markup = reply_markup
