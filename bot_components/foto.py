import logging
import random
import threading
from os import listdir
from typing import Optional

from telegram import Message, Chat

from utils.os_utils import get_json_data_from_file, get_absolute_path
import utils.regex_parser as parser


class Foto:
    keywords: dict[str, list[str]] = None
    chat_specific_removal_seconds: dict[int, float] = {}

    @classmethod
    def init(cls):
        cls.keywords = get_json_data_from_file("keyword_foto.json")

    @classmethod
    def handle_message(cls, text: str, chat: Chat):
        res: Optional[Message] = None

        if cls.keywords is None:
            return

        for category, lst in cls.keywords.items():
            if any(parser.contains(s, text) for s in lst):
                res = chat.send_photo(cls.__get_random_photo(category))
                seconds = cls.chat_specific_removal_seconds.get(chat.id, 5)
                threading.Timer(seconds, lambda: res.delete()).start()

    @classmethod
    def __get_random_photo(cls, category: str) -> bytes:
        directory = get_absolute_path(f"/resources/photos/{category}")
        random_photo = f"{directory}/{random.choice(listdir(directory))}"
        try:
            with open(random_photo, "rb") as photo:
                return photo.read()
        except FileNotFoundError:
            logging.warning(f"Photo '{random_photo}' not found!")
