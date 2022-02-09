from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, MessageHandler, Filters

from bot_component.foto import Foto
from bot_component.insulti import Insulti
from bot_component.risposte import Risposte


class Gestore:
    @staticmethod
    def __gestisci(update: Update, context: CallbackContext):
        Foto.command_handler_foto(update, context)
        Risposte.command_handler_risposte(update, context)
        Insulti.command_handler_insulti(update, context)

    @staticmethod
    def init(dispatcher: Dispatcher):
        dispatcher.add_handler(MessageHandler(
            Filters.text, Gestore.__gestisci, pass_user_data=True, run_async=True))
