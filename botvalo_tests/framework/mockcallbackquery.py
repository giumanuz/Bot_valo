class MockCallbackQuery:
    def __init__(self, data: str):
        self.answered = False
        self._data = data

    @property
    def data(self):
        return self._data

    def answer(self):
        self.answered = True

    def _has_been_answered(self):
        return self.answered
