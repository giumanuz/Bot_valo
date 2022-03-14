import re

from telegram import Chat
from telegram.ext import CallbackContext

from bot_components.db.db_manager import Database

patternRegistraRimuovi = re.compile(r"^botvalo (registra|rimuovi) chat ([a-z0-9_-]+)")
patternScrivi = re.compile(r"^botvalo scrivi a ([a-z0-9_-]+) (.+)$")


class Messaggi:
    @classmethod
    def handle_message(cls, text: str, chat: Chat, context: CallbackContext):
        match = patternRegistraRimuovi.search(text)
        if match is not None:
            comando = match.group(1)
            chat_name = match.group(2)
            chat_id = chat.id
            if comando == "registra":
                Database.get().set_chat_alias(chat_name, chat_id)
                chat.send_message("Chat registrata correttamente")
            elif comando == "rimuovi":
                Database.get().remove_chat_alias(chat_name)
                chat.send_message("Chat rimossa correttamente")
            return

        match = patternScrivi.search(text)
        if match:
            chat_name = match.group(1)
            message = match.group(2)
            chat_id = Database.get().get_chat_aliases().get(chat_name, None)
            if chat_id is None:
                chat.send_message(f"Non esiste nessuna chat {chat_name}")
                return
            context.bot.send_message(chat_id=chat_id, text=message)
