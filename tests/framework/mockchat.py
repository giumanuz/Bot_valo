class MockChat:
    def __init__(self, chat_id: int = -1):
        self._id = chat_id

    @property
    def id(self):
        return self._id
