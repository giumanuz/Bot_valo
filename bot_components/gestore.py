from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, MessageHandler, Filters

from bot_components.foto import Foto
from bot_components.insulti import Insulti
from bot_components.risposte import Risposte


def _inoltra_messaggio(update: Update, context: CallbackContext):
    print(update.message.from_user.first_name, update.message.from_user.id)
    Foto.handle_message(update, context)
    Risposte.handle_message(update, context)
    Insulti.handle_message(update, context)


def add_message_handlers(dispatcher: Dispatcher):
    dispatcher.add_handler(MessageHandler(
        Filters.text, _inoltra_messaggio, pass_user_data=True, run_async=True))
