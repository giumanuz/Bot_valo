import random
import re

from telegram import Chat

from bot_components.db.db_manager import Database


class Insulti:
    lista_insulti = None

    @classmethod
    def init(cls):
        Database.get().register_for_config_changes("insulti", cls._init_lista_insulti)

    @classmethod
    def _init_lista_insulti(cls):
        cls.lista_insulti = Database.get().get_lista_insulti()

    @classmethod
    def handle_message(cls, text: str, chat: Chat):
        if cls.lista_insulti is None:
            return
        s = re.search(r"(^| )insulta (.*?)$", text)
        if s is not None:
            chat.send_message(
                random.choice(cls.lista_insulti).format(s.group(2))
            )
