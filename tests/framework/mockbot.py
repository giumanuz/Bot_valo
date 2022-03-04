from tests.framework.mockmessage import MockMessage


class MockBot:
    def __init__(self):
        self._result: list[dict] = []
        self.response_message_id = 2

    @property
    def result(self):
        return self._result.copy()

    def send_photo(self, chat_id=-1, photo: bytes = None):
        data = {'chat_id': chat_id, 'photo': photo}
        self._result.append(data)

    def send_message(self,
                     chat_id=-1,
                     text: str = None,
                     reply_markup=None):
        data = {'chat_id': chat_id, 'text': text}
        if reply_markup:
            data['reply_markup'] = reply_markup
        self._result.append(data)
        return MockMessage(text, message_id=self.response_message_id, reply_markup=reply_markup)

    def reset_data(self):
        self._result = []
        self.response_message_id = -1
