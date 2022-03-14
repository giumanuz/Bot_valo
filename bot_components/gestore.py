from telegram import Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CallbackContext

from bot_components.foto import Foto
from bot_components.insulti import Insulti
from bot_components.messaggi import Messaggi
from bot_components.risposte import Risposte
from utils.telegram_utils import get_effective_text


def add_message_handlers(dispatcher: Dispatcher):
    dispatcher.add_handler(MessageHandler(
        filters=Filters.text | Filters.caption,
        callback=inoltra_messaggio,
        pass_user_data=True,
        run_async=True)
    )


def inoltra_messaggio(update: Update, context: CallbackContext = None):
    if has_invalid_message(update):
        return
    text, chat = get_effective_text(update), update.effective_chat
    if "botvalo timer" in text:
        Foto.set_chat_removal_timer(text, chat)
        return
    Risposte.handle_message(text, chat)
    Insulti.handle_message(text, chat)
    Foto.handle_message(text, chat)
    Messaggi.handle_message(text, chat, context)


def has_invalid_message(update):
    return update.edited_message is not None or update.effective_message.text is None
