import random
import re
from utils.os_utils import get_json_data_from_file

from telegram import Chat


class Insulti:
    lista_insulti = None

    @classmethod
    def init(cls):
        cls.lista_insulti = get_json_data_from_file("insulti.json")

    @classmethod
    def handle_message(cls, text: str, chat: Chat):
        if cls.lista_insulti is None:
            return
        s = re.search(r"(^| )insulta (.*?)$", text)
        if s is not None:
            chat.send_message(
                random.choice(cls.lista_insulti).format(s.group(2))
            )
