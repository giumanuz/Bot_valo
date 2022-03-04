import json
import logging
import random

from telegram import Chat

from utils.os_utils import path_to_text_file
from utils.regex_parser import contains


class Risposte:
    dict_risposte = {}
    __ALTERNATIVE_WORD = "ALT::"

    @classmethod
    def init(cls):
        try:
            cls._init()
        except OSError:
            logging.error("File not found: risposte.json")

    @classmethod
    def _init(cls):
        with open(path_to_text_file("risposte.json"), 'r', encoding="UTF-8") as f:
            cls.dict_risposte = json.load(f)

    @classmethod
    def handle_message(cls, text: str, chat: Chat):
        for trigger in cls.dict_risposte:
            if contains(trigger, text):
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
