from telegram import Chat
import re

from telegram.ext import CallbackContext

from bot_components.db.db_manager import Database

class Messaggi:
    @classmethod
    def handle_message(cls, text: str, chat: Chat, context: CallbackContext):
        match = re.search(r"^botvalo (registra|rimuovi) chat ([a-z0-9_-]+)", text)
        if match is not None:
            comando = match.group(0)
            chat_name = match.group(1)
            chat_id = chat.id
            if comando == "registra":
                Database.get().set_chat_alias(chat_name, chat_id)
                chat.send_message("Chat registrata correttamente")
            elif comando == "rimuovi":
                Database.get().delete_chat_alias(chat_name)
                chat.send_message("Chat rimossa correttamente")
            return

        match = re.search(r"^botvalo scrivi a ([a-z0-9_-]+) (.+)$", text)
        if match is not None:
            chat_name = match.group(0)
            message = match.group(1)
            chat_id = Database.get().get_dict_alias_chat().get(chat_name, None)
            if chat_id is None:
                chat.send_message(f"Non esiste nessuna chat {chat_name}")
                return
            context.bot.send_message(chat_id=chat_id, text=message)
