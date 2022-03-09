class MockChat:

    __COMMON_BOT = None
    __COMMON_CHAT = None

    def __init__(self, chat_id: int = -1):
        self._id = chat_id

    @property
    def id(self):
        return self._id

    def send_message(self, text, reply_markup=None):
        self.__COMMON_BOT.send_message(chat_id=self._id,
                                       text=text,
                                       reply_markup=reply_markup)

    def send_photo(self, photo):
        self.__COMMON_BOT.send_photo(chat_id=self._id,
                                     photo=photo)

    @classmethod
    def _SET_COMMON_BOT(cls, bot):
        cls.__COMMON_BOT = bot

    @classmethod
    def common(cls):
        if cls.__COMMON_CHAT is None:
            cls.__COMMON_CHAT = cls(-1)
        return cls.__COMMON_CHAT
