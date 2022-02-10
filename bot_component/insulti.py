import json
import logging
import random

from telegram import Update
from telegram.ext import CallbackContext


class Insulti:
    lista_insulti = None
    try:
        with open('./File/insulti.json', 'r') as f:
            lista_insulti = json.load(f)
        logging.debug("insulti.json loaded correctly.")
    except json.JSONDecodeError:
        logging.warning("Unable to load json from file.")

    @staticmethod
    def command_handler_insulti(update: Update, context: CallbackContext):
        testo = str(update.effective_message.text).lower()

        if "insulta" in testo:
            if Insulti.lista_insulti is None:
                logging.error("lista_insulti not loaded correctly from json file.")
                return
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'Cioppy {random.choice(Insulti.lista_insulti)}')
