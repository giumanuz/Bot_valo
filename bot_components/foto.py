import threading

from telegram import Chat

from bot_components.db.db_manager import Database
from utils.os_utils import get_current_local_datetime, get_current_weekday_name
from utils.regex_parser import WordParser


class Foto:
    keywords: dict[str, list[str]] = {}
    blacklisted_hours: dict[str, list[int]] = {}
    SECONDS_INFINITE = 99999

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
        for category, lst in cls.keywords.items():
            if any(WordParser.contains(s, text) for s in lst):
                random_photo = cls.__get_random_photo(category)
                res = chat.send_photo(random_photo)
                if not res:
                    return
                seconds = Database.get().get_chat_removal_seconds(chat.id)
                if seconds == cls.SECONDS_INFINITE:
                    return
                threading.Timer(seconds, lambda: res.delete() if res else None).start()

    @classmethod
    def __get_random_photo(cls, category: str) -> bytes:
        return Database.get().get_random_photo(category)

    @classmethod
    def set_chat_removal_timer(cls, chat, seconds):
        try:
            Database.get().set_chat_removal_seconds(chat.id, float(seconds))
        except (TypeError, AttributeError):
            raise AttributeError()

    @classmethod
    def hour_in_blacklist(cls) -> bool:
        now_hour = get_current_local_datetime().hour
        current_weekday_name = get_current_weekday_name()
        if current_weekday_name not in cls.blacklisted_hours:
            return False
        forbidden_hour_interval = cls.blacklisted_hours[current_weekday_name]
        return forbidden_hour_interval[0] <= now_hour < forbidden_hour_interval[1]
