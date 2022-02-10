import json
import logging
import random

from telegram import Update
from telegram.ext import CallbackContext


class Insulti:
    lista_insulti = None
    try:
        with open('./resources/text_files/insulti.json', 'r') as f:
            lista_insulti = json.load(f)
        logging.debug("insulti.json loaded correctly.")
    except json.JSONDecodeError:
        logging.error("Unable to load json from file.")
    except FileNotFoundError:
        logging.error("File insulti.json not found.")

    @classmethod
    def command_handler_insulti(cls, update: Update, context: CallbackContext):
        testo = str(update.effective_message.text).lower()

        if cls.lista_insulti is None:
            return

        if "insulta" in testo:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'Cioppy {random.choice(cls.lista_insulti)}')
