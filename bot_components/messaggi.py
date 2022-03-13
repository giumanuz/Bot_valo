from telegram import Chat, Update
import re

from telegram.ext import CallbackContext

from bot_components.db.db_manager import Database


class Messaggi:
    @classmethod
    def handle_message(cls, text: str, chat: Chat, context: CallbackContext):
        match = re.search(r"^botvalo registra chat ([a-z0-9_-]+)", text)
        if match is not None:
            chat_name = match.groups()[0]
            chat_id = chat.id
            Database.get().set_chat_alias(chat_name, chat_id)
            return

        match = re.search(r"^botvalo scrivi a ([a-z0-9_-]+) (.+)$", text)
        if match is not None:
            chat_name = match.groups()[0]
            message = match.groups()[1]
            chat_id = Database.get().get_dict_alias_chat().get(chat_name, None)
            if chat_id is None:
                chat.send_message(f"Non esiste nessuna chat {chat_name}")
                return
            context.bot.send_message(chat_id=chat_id, text=message)
