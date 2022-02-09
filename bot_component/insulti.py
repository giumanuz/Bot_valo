import json
import random
from telegram import Update
from telegram.ext import CallbackContext

lista_insulti = json.load(open('./File/insulti.json', 'r'))

class Insulti:
    @staticmethod
    def command_handler_insulti(update: Update, context: CallbackContext):
        testo = str(update.effective_message.text).lower()

        if "insulta" in testo:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'Cioppy {random.choice(lista_insulti)}')
