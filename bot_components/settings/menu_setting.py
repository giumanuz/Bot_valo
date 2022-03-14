from abc import abstractmethod, ABC as ABSTRACT_CLASS

from telegram import Update
from telegram.ext import Dispatcher, CallbackQueryHandler


class MenuSetting(ABSTRACT_CLASS):
    name: str = ...
    id: str = ...

    @classmethod
    def register(cls, dispatcher: Dispatcher):
        cls.init(dispatcher)
        dispatcher.add_handler(CallbackQueryHandler(
            cls.callback,
            pattern=f"^{cls.id}$",
            run_async=True
        ))

    @classmethod
    @abstractmethod
    def init(cls, dispatcher: Dispatcher):
        ...

    @classmethod
    @abstractmethod
    def callback(cls, update: Update, dispatcher: Dispatcher):
        ...
