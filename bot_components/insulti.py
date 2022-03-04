import json
import logging
import random
import re
from os import path

from telegram import Chat


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
    def handle_message(cls, text: str, chat: Chat):
        if cls.lista_insulti is None:
            return
        s = re.search(r"(^| )insulta (.*?)$", text)
        if s is not None:
            chat.send_message(
                random.choice(cls.lista_insulti).format(s.group(2))
            )
