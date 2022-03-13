from telegram import Chat, Update
import re

from telegram.ext import CallbackContext

mio_dic = {}


class Messaggi:
    @classmethod
    def handle_message(cls, text: str, chat: Chat, context: CallbackContext):
        match = re.search(r"^botvalo registra chat ([a-z0-9_-]+)", text)
        if match is not None:
            print("mi hanno chiamato, ", match.group())
            chat_name = match.group()
            chat_id = chat.id
            mio_dic[chat_name] = chat_id
            return

        match = re.search(r"^botvalo scrivi a ([a-z0-9_-]+) (.+)$", text)
        if match is not None:
            chat_name = match.groups()[0]
            message = match.groups()[1]
            chat_id = mio_dic.get(chat_name, None)
            print("manda messaggio ", chat_id)
            if chat_id is None:
                chat.send_message(f"Non esiste nessuna chat {chat_name}")
                return
            context.bot.send_message(chat_id=chat_id, text=message)
