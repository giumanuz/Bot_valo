class MockContext:
    def __init__(self, dispatcher):
        self._dispatcher = dispatcher

    @property
    def bot(self):
        return self._dispatcher.bot
