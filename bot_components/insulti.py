import json
import logging
import random
from os import path

from telegram import Update
from telegram.ext import CallbackContext


class Insulti:
    lista_insulti = None

    @classmethod
    def initialize(cls):
        path_to_json = path.join(path.dirname(__file__), "..", "resources", "text_files", "insulti.json")
        try:
            with open(path_to_json, 'r') as f:
                cls.lista_insulti = json.load(f)
            logging.info("insulti.json loaded correctly.")
        except json.JSONDecodeError:
            logging.error("Unable to load json from file.")
        except FileNotFoundError:
            logging.error("File insulti.json not found.")

    @classmethod
    def is_initialized(cls):
        return cls.lista_insulti is not None

    @classmethod
    def command_handler_insulti(cls, update: Update, context: CallbackContext):
        testo = str(update.effective_message.text).lower()
        if not cls.is_initialized():
            logging.error("Insulti class must be initialized first "
                          "with Insulti.initialize()")
            return

        if "insulta" in testo:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'Cioppy {random.choice(cls.lista_insulti)}')
