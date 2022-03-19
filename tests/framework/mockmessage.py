from telegram import InlineKeyboardMarkup


class MockMessage:
    __COMMON_BOT = None

    def __init__(self,
                 text,
                 message_id=-1,
                 reply_markup: InlineKeyboardMarkup = None,
                 caption=None,
                 chat_id=-1):
        self._text = text
        self._message_id = message_id
        self._reply_markup = reply_markup
        self._caption = caption
        self._chat_id = chat_id
        self._deleted = False
        self._exception_on_delete = None

    @classmethod
    def _SET_COMMON_BOT(cls, bot):
        cls.__COMMON_BOT = bot

    @property
    def text(self):
        return self._text

    @property
    def message_id(self):
        return self._message_id

    @property
    def reply_markup(self):
        return self._reply_markup

    @property
    def caption(self):
        return self._caption

    @property
    def chat_id(self):
        return self._chat_id

    def edit_reply_markup(self, reply_markup: InlineKeyboardMarkup):
        self._reply_markup = reply_markup

    def reply_text(self, text, reply_markup=None):
        self.__COMMON_BOT.send_message(chat_id=self._chat_id, text=text, reply_markup=reply_markup)

    def reply_photo(self, photo):
        self.__COMMON_BOT.send_photo(chat_id=self.chat_id, photo=photo)

    def delete(self):
        if self._exception_on_delete:
            raise self._exception_on_delete
        else:
            self._deleted = True

    def _set_exception_on_delete(self, exception_type):
        self._exception_on_delete = exception_type
