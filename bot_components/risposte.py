import logging
import random

from telegram import Chat

from bot_components.db.db_manager import Database
from utils.regex_parser import WordParser


class Risposte:
    dict_risposte = None
    __ALTERNATIVE_WORD = "ALT::"

    @classmethod
    def init(cls):
        db = Database.get()
        db.register_for_config_changes("risposte", cls._init_lista_risposte)

    @classmethod
    def _init_lista_risposte(cls):
        cls.dict_risposte = Database.get().get_risposte()

    @classmethod
    def handle_message(cls, text: str, chat: Chat):
        for trigger in cls.dict_risposte:
            if WordParser.contains(trigger, text):
                value = cls.get_actual_value(trigger)
                chat.send_message(
                    value if type(value) is str else random.choice(value)
                )

    @classmethod
    def get_actual_value(cls, trigger):
        value = cls.dict_risposte[trigger]
        if type(value) is str and value.startswith(cls.__ALTERNATIVE_WORD):
            try:
                return cls.dict_risposte[value[5:]]
            except KeyError:
                logging.warning(f"Non c'è l'alternativa \"{value[5:]}\" di \"{trigger}\"")
        return value
