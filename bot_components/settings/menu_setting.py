from abc import abstractmethod, ABC as ABSTRACT_CLASS

from telegram import Update, InlineKeyboardButton
from telegram.ext import Dispatcher, CallbackQueryHandler, CallbackContext


class MenuSetting(ABSTRACT_CLASS):

    @property
    @abstractmethod
    def name(self):
        ...

    @property
    @abstractmethod
    def id(self):
        ...

    @abstractmethod
    def __init__(self, dispatcher: Dispatcher):
        self.dispatcher = dispatcher
        self.dispatcher.add_handler(CallbackQueryHandler(
            self.callback,
            pattern=f"^{self.id}$",
            run_async=True
        ))
        ...

    @abstractmethod
    def callback(self, update: Update, context: CallbackContext):
        ...

    def add_callback_query_handler(self, callback, *args):
        handler = CallbackQueryHandler(
            callback,
            pattern=self.pattern(*args)
        )
        self.dispatcher.add_handler(handler)
        return handler

    def pattern(self, *args, is_regex=True):
        tokens = "-".join(str(x) for x in args).lower()
        pattern = f"{self.id}-{tokens}"
        if is_regex:
            return fr"^{pattern}$"
        return pattern

    def new_button(self, name: str, *args):
        return InlineKeyboardButton(name, callback_data=self.pattern(*args, is_regex=False))
