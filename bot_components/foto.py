import logging
import random
import threading
from os import listdir

from telegram import Chat

from utils.os_utils import get_json_data_from_file, get_absolute_path
from utils.regex_parser import WordParser


class Foto:
    keywords: dict[str, list[str]] = {}
    chats_removal_seconds: dict[int, float] = {}
    __DEFAULT_REMOVAL_SECONDS = 5

    @classmethod
    def init(cls):
        cls.keywords = get_json_data_from_file("keyword_foto.json")

    @classmethod
    def handle_message(cls, text: str, chat: Chat):
        for category, lst in cls.keywords.items():
            if any(WordParser.contains(s, text) for s in lst):
                res = chat.send_photo(cls.__get_random_photo(category))
                if res:
                    seconds = cls.chats_removal_seconds.get(chat.id, cls.__DEFAULT_REMOVAL_SECONDS)
                    threading.Timer(seconds, lambda: res.delete() if res else None).start()

    @classmethod
    def __get_random_photo(cls, category: str) -> bytes:
        directory = get_absolute_path(f"/resources/photos/{category}")
        random_photo = f"{directory}/{random.choice(listdir(directory))}"
        try:
            with open(random_photo, "rb") as photo:
                return photo.read()
        except FileNotFoundError:
            logging.warning(f"Photo '{random_photo}' not found!")
