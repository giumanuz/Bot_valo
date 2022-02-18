import json
import logging
import random
from os import path

from telegram import Update
from telegram.ext import CallbackContext


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
    def handle_message(cls, update: Update, context: CallbackContext):
        testo = str(update.effective_message.text).lower()
        if cls.lista_insulti is None:
            return
        if "insulta" in testo:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'Cioppy {random.choice(cls.lista_insulti)}')
