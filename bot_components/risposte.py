import logging
import random

from telegram import Chat

from utils.os_utils import get_json_data_from_file
from utils.regex_parser import WordParser


class Risposte:
    dict_risposte = None
    __ALTERNATIVE_WORD = "ALT::"

    @classmethod
    def init(cls):
        cls.dict_risposte = get_json_data_from_file("risposte.json")

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
