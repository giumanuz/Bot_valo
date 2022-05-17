from telegram import InlineKeyboardMarkup

from botvalo_tests.framework.mockcallbackquery import MockCallbackQuery
from botvalo_tests.framework.mockchat import MockChat
from botvalo_tests.framework.mockmessage import MockMessage
from botvalo_tests.framework.mockuser import MockUser


class MockUpdate:
    def __init__(self,
                 chat: MockChat = None,
                 message: MockMessage = None,
                 user: MockUser = None,
                 callback_query: MockCallbackQuery = None):
        self._message = message if message is not None else MockMessage("")
        self._chat = chat if chat is not None else MockChat()
        self._user = user if user is not None else MockUser()
        self._callback_query = callback_query if callback_query is not None else MockCallbackQuery("")
        self._edited_message = None

    @property
    def effective_message(self):
        return self._message

    @property
    def effective_chat(self):
        return self._chat

    @property
    def effective_user(self):
        return self._user

    @property
    def callback_query(self):
        return self._callback_query

    @property
    def edited_message(self):
        return self._edited_message

    def _edit_message(self, edited_text=""):
        self._edited_message = self._message
        self._edited_message._text = edited_text
        self._message = None

    # Constructors

    @classmethod
    def from_message(cls, message: str, message_id=-1) -> 'MockUpdate':
        return cls(message=MockMessage(message, message_id))

    @classmethod
    def create_from(cls, user_first_name="",
                    message="",
                    chat_id=-1,
                    callback_data="",
                    user_id=-1,
                    message_id=-1,
                    markup: InlineKeyboardMarkup = None) -> 'MockUpdate':
        return cls(chat=MockChat(chat_id),
                   user=MockUser(user_id, user_first_name),
                   message=MockMessage(message, message_id, markup),
                   callback_query=MockCallbackQuery(callback_data))

    @classmethod
    def empty(cls) -> 'MockUpdate':
        return cls()
