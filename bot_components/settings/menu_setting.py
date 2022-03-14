from abc import abstractmethod, ABC as ABSTRACT_CLASS

from telegram import Update
from telegram.ext import Dispatcher, CallbackQueryHandler


class MenuSetting(ABSTRACT_CLASS):

    def register(self):
        self.dispatcher.add_handler(CallbackQueryHandler(
            self.callback,
            pattern=f"^{self.id}$",
            run_async=True
        ))

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
        ...

    @abstractmethod
    def callback(self, update: Update, dispatcher: Dispatcher):
        ...
