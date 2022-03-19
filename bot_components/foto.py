import logging
import threading
from queue import Queue

from telegram import Chat
from telegram.error import TimedOut, BadRequest

from bot_components.db.db_manager import Database
from utils.os_utils import get_current_local_datetime, get_current_weekday_name
from utils.regex_parser import WordParser


class Foto:
    keywords: dict[str, list[str]] = {}
    blacklisted_hours: dict[str, list[int]] = {}
    SECONDS_INFINITE = 99999
    queue = Queue()

    @classmethod
    def init(cls):
        db = Database.get()
        db.register_for_config_changes("keyword_foto", cls._init_keywords)
        db.register_for_config_changes("schedule_blacklist", cls._init_blacklist)

    @classmethod
    def _init_keywords(cls):
        cls.keywords = Database.get().get_keyword_foto()

    @classmethod
    def _init_blacklist(cls):
        cls.blacklisted_hours = Database.get().get_schedule_blacklist()

    @classmethod
    def _empty_blacklist(cls):
        cls.blacklisted_hours = {}

    @classmethod
    def _full_blacklist(cls):
        cls.blacklisted_hours = {"monday": [0, 24], "tuesday": [0, 24], "wednesday": [0, 24], "thursday": [0, 24],
                                 "friday": [0, 24], "saturday": [0, 24], "sunday": [0, 24]}

    @classmethod
    def handle_message(cls, text: str, chat: Chat):
        if cls.hour_in_blacklist():
            return
        seconds = Database.get().get_chat_removal_seconds(chat.id)
        for category, lst in cls.keywords.items():
            if cls._text_in_list(text, lst):
                random_photo = cls.__get_random_photo(category)
                res = chat.send_photo(random_photo)
                if seconds != cls.SECONDS_INFINITE:
                    cls.delete_message_after_seconds(res, seconds)

    @classmethod
    def _text_in_list(cls, text, lst):
        return any(WordParser.contains(s, text) for s in lst)

    @classmethod
    def delete_message_after_seconds(cls, message, seconds: int):
        if message:
            threading.Timer(seconds, cls._delete_message, [message]).start()

    @classmethod
    def _delete_message(cls, message):
        try:
            if message:
                message.delete()
        except BadRequest:
            logging.warning(f"Message not deleted: {message}")
        except TimedOut:
            logging.warning(f"Timed out, message not deleted: {message}")

    @classmethod
    def __get_random_photo(cls, category: str) -> bytes:
        return Database.get().get_random_photo(category)

    @classmethod
    def set_chat_removal_timer(cls, chat, seconds):
        try:
            Database.get().set_chat_removal_seconds(chat.id, float(seconds))
        except TypeError:
            raise TypeError()

    @classmethod
    def hour_in_blacklist(cls) -> bool:
        now_hour = get_current_local_datetime().hour
        current_weekday_name = get_current_weekday_name()
        if current_weekday_name not in cls.blacklisted_hours:
            return False
        forbidden_hour_interval = cls.blacklisted_hours[current_weekday_name]
        return forbidden_hour_interval[0] <= now_hour < forbidden_hour_interval[1]
