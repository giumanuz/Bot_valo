import json
import logging
import random
from os import path

from telegram import Update

import utils.regex_parser as parser
import utils.telegram_utils as tgutils


def fetch_insulti():
    lista_insulti = None
    path_to_json = path.join(path.dirname(__file__), "..", "resources", "text_files", "insulti.json")
    try:
        with open(path_to_json, 'r', encoding='UTF-8') as f:
            lista_insulti = json.load(f)
        logging.info("insulti.json loaded correctly.")
    except json.JSONDecodeError:
        logging.error("Unable to load json from file.")
    except FileNotFoundError:
        logging.error("File insulti.json not found.")
    return lista_insulti


class Insulti:
    lista_insulti = fetch_insulti()

    @classmethod
    def handle_message(cls, update: Update):
        testo = tgutils.get_effective_text(update)
        if cls.lista_insulti is None:
            return
        if parser.contains("insulta", testo):
            update.effective_message.reply_text(f'Cioppy {random.choice(cls.lista_insulti)}')
