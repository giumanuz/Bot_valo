import json
import logging
import random

from telegram import Update

import utils.telegram_utils as tgutils
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
    def handle_message(cls, update: Update):
        testo = tgutils.get_effective_text(update)
        for trigger in cls.dict_risposte:
            if contains(trigger, testo):
                value = cls.get_actual_value(trigger)
                update.effective_message.reply_text(
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
