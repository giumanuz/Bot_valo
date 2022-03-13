from telegram.ext import Handler


class MockDispatcher:
    def __init__(self, bot):
        self._bot = bot
        self.handlers: list[Handler] = []

    def add_handler(self, handler):
        self.handlers.append(handler)

    @property
    def bot(self):
        return self._bot
