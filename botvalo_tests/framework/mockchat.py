class MockChat:

    __COMMON_BOT = None
    __COMMON_CHAT = None

    PRIVATE = 1
    GROUP = 2
    CHANNEL = 3
    SUPERGROUP = 4

    def __init__(self, chat_id: int = -1):
        self._id = chat_id
        self._type = self.PRIVATE

    @property
    def id(self):
        return self._id

    @property
    def type(self):
        from telegram import Chat
        if self._type == self.PRIVATE:
            return Chat.PRIVATE
        elif self._type == self.GROUP:
            return Chat.GROUP
        elif self._type == self.SUPERGROUP:
            return Chat.SUPERGROUP
        elif self._type == self.CHANNEL:
            return Chat.CHANNEL
        else:
            raise AttributeError(f"Invalid chat type.")

    @type.setter
    def type(self, chat_type):
        self._type = chat_type

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
