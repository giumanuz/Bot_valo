class MockBot:
    def __init__(self):
        self._result = []

    @property
    def result(self):
        return self._result.copy()

    def sendPhoto(self, chat_id=-1, photo: bytes = None):
        data = {'chat_id': chat_id, 'photo': photo}
        self._result.append(data)

    def send_message(self, chat_id=-1, text: str = None):
        data = {'chat_id': chat_id, 'text': text}
        self._result.append(data)

    def reset_data(self):
        self._result = []


class MockContext:
    def __init__(self, dispatcher):
        self._dispatcher = dispatcher

    @property
    def bot(self):
        return self._dispatcher.bot


class MockDispatcher:
    def __init__(self, bot):
        self._bot = bot
        self.handlers = []

    def add_handler(self, handler):
        self.handlers.append(handler)

    @property
    def bot(self):
        return self._bot


class MockMessage:
    def __init__(self, text):
        self._text = text

    @property
    def text(self):
        return self._text


class MockUpdate:
    def __init__(self, message: MockMessage):
        self._message = message
        self._chat = MockChat

    @property
    def effective_message(self):
        return self._message

    @property
    def effective_chat(self):
        return self._chat


class MockUpdater:
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def start_polling(self):
        pass


class MockChat:
    @property
    def id(self):
        return -1
