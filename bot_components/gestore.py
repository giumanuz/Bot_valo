from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, MessageHandler, Filters

from bot_components.foto import Foto
from bot_components.insulti import Insulti
from bot_components.risposte import Risposte


def _gestisci(update: Update, context: CallbackContext):
    Foto.command_handler_foto(update, context)
    Risposte.command_handler_risposte(update, context)
    Insulti.command_handler_insulti(update, context)


def add_message_handlers(dispatcher: Dispatcher):
    if not Insulti.is_initialized():
        Insulti.initialize()
    dispatcher.add_handler(MessageHandler(
        Filters.text, _gestisci, pass_user_data=True, run_async=True))
