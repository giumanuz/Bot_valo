import threading
from datetime import timedelta

import telegram.error
from telegram import Chat, Update, User

import utils.os_utils
from bot_components.db.db_manager import Database
from utils.regex_parser import WordParser


class AntiCioppyPolicy:
    timeout_words_list = list()
    timeout_user_alerts = {}
    max_alerts = 2
    min_ban_time_in_minutes: int = 5  # Warning: must be > 1
    BAN_MESSAGE = "Bannato {name} per {minutes} minuti!"
    BAN_ERROR_MESSAGE = "Non sono riuscito a bannare quel troione di {name}. Forse mi mancano dei permessi?"
    WARN_MESSAGE = "E basta co' sti discorsi! Avvertimento {current_warns} di {max_warns}, e poi ti banno!"

    BAN_PRIVATE_MESSAGE = "Sei stato bannato per {minutes} minuti. Sarai sbannato il {date} alle {hour}."
    UNBAN_PRIVATE_MESSAGE = "Sei stato sbannato dal gruppo {group_name}! Prova ad entrare con questo link: {link}"

    @classmethod
    def init(cls):
        Database.get().register_for_config_changes("timeout_sensitive_words", cls._init_timeout_words_list)

    @classmethod
    def _init_timeout_words_list(cls):
        cls.timeout_words_list = Database.get().get_timeout_words()

    @classmethod
    def handle_message(cls, text: str, chat: Chat, update: Update):
        if chat.type == Chat.PRIVATE:
            return
        if any(WordParser.contains(text, e) for e in cls.timeout_words_list):
            user = update.effective_user
            cls.timeout_user_alerts.setdefault(user.id, 0)
            cls.timeout_user_alerts[user.id] += 1
            user_alerts = cls.timeout_user_alerts[user.id]
            if user_alerts > cls.max_alerts:
                cls.try_to_timeout_member(chat, user)
            else:
                cls.warn_member(user_alerts, update)

    @classmethod
    def try_to_timeout_member(cls, chat: Chat, user: User):
        try:
            ban_minutes = cls.get_ban_minutes(user.id)
            unban_date = cls.get_unban_date(ban_minutes)
            cls.ban_chat_member(chat, user.id, until_date=unban_date)
            cls.timeout_user_alerts.pop(user.id)
            chat.send_message(cls.BAN_MESSAGE.format(name=user.full_name,
                                                     minutes=ban_minutes))
            user.send_message(cls.BAN_PRIVATE_MESSAGE.format(minutes=ban_minutes,
                                                             date=unban_date.strftime("%d/%m"),
                                                             hour=unban_date.strftime("%H:%M")))
            threading.Timer(ban_minutes * 60, user.send_message,
                            args=[cls.UNBAN_PRIVATE_MESSAGE.format(group_name=chat.title,
                                                                   link=chat.create_invite_link(
                                                                       member_limit=1
                                                                   ).invite_link)]
                            ).start()
        except CannotBanMember:
            chat.send_message(cls.BAN_ERROR_MESSAGE.format(name=user.full_name))

    @classmethod
    def get_ban_minutes(cls, user_id):
        ban_times = Database.get().get_ban_times(user_id) + 1
        return cls.min_ban_time_in_minutes * ban_times

    @classmethod
    def get_unban_date(cls, minutes):
        time_now = utils.os_utils.get_current_local_datetime()
        return time_now + timedelta(minutes=minutes)

    @classmethod
    def ban_chat_member(cls, chat: Chat, member_id, until_date):
        try:
            success = chat.ban_member(member_id, until_date=until_date)
            if not success:
                raise CannotBanMember()
        except telegram.error.BadRequest:
            raise CannotBanMember()

    @classmethod
    def warn_member(cls, alerts, update: Update):
        update.effective_message.reply_text(
            cls.WARN_MESSAGE.format(current_warns=alerts,
                                    max_warns=cls.max_alerts)
        )


class CannotBanMember(Exception):
    pass
