from telegram import Update
from telegram.ext import Dispatcher, MessageHandler, Filters

from bot_components.anti_cioppy_policy import AntiCioppyPolicy
from bot_components.foto import Foto
from bot_components.insulti import Insulti
from bot_components.risposte import Risposte
from utils.telegram_utils import get_effective_text


def add_message_handlers(dispatcher: Dispatcher):
    dispatcher.add_handler(MessageHandler(
        filters=(Filters.text | Filters.caption) & ~Filters.update.edited_message,
        callback=inoltra_messaggio,
        pass_user_data=True,
        run_async=True)
    )


def inoltra_messaggio(update: Update, _=None):
    text, chat = get_effective_text(update), update.effective_chat
    Risposte.handle_message(text, chat)
    Insulti.handle_message(text, chat)
    Foto.handle_message(text, chat)
    AntiCioppyPolicy.handle_message(text, chat, update)
