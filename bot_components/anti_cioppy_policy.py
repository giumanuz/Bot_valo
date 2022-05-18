import threading
from datetime import timedelta
from math import ceil

import telegram.error
from telegram import Chat, Update, User

import utils.os_utils
from bot_components.db.db_manager import Database as Db


class AntiCioppyPolicy:
    timeout_words_list = []
    initial_ban_time_in_minutes: int = 8

    timeout_alerts = 0
    CIOPPY_USER_ID = 364369396

    BAN_MESSAGE = "Bannato cioppy per {minutes} minuti!"
    BAN_ERROR_MESSAGE = "Non sono riuscito a bannare quel troione di cioppy. Forse mi mancano dei permessi?"
    WARN_MESSAGE = "E basta co' sti discorsi! Avvertimento {current_warns} di {max_warns}, e poi ti banno!"

    BAN_PRIVATE_MESSAGE = "Sei stato bannato per {minutes} minuti per aver fatto discorsi del cazzo, come al solito. " \
                          "Sarai sbannato il {date} alle {hour}. Te lo ricorderò."
    UNBAN_PRIVATE_MESSAGE = "Sei stato sbannato dal gruppo {group_name}, prova a rientrare con questo link: {link}"

    @classmethod
    def init(cls):
        cls.initial_ban_time_in_minutes = max(1, cls.initial_ban_time_in_minutes)
        Db.get().register_for_config_changes("timeout_sensitive_words", cls._init_timeout_words_list)

    @classmethod
    def _init_timeout_words_list(cls):
        cls.timeout_words_list = Db.get().get_cioppy_blacklist_words()

    @classmethod
    def handle_message(cls, text: str, chat: Chat, update: Update):
        user = update.effective_user
        if user.id != cls.CIOPPY_USER_ID or chat.type == Chat.PRIVATE:
            return
        if cls.contains_a_timeout_word(text):
            cls.timeout_alerts += 1
            max_alerts = Db.get().get_cioppy_max_alerts()
            if cls.timeout_alerts > max_alerts:
                cls.try_to_timeout_member(chat, user)
            else:
                cls.warn_member(max_alerts, update)

    @classmethod
    def contains_a_timeout_word(cls, text):
        return any(e in text for e in cls.timeout_words_list)

    @classmethod
    def try_to_timeout_member(cls, chat: Chat, user: User):
        try:
            cls._timeout_member(chat, user)
        except CannotBanMember:
            cls.send_error_message(chat)

    @classmethod
    def _timeout_member(cls, chat, user):
        ban_minutes = cls.get_ban_minutes()
        unban_date = cls.get_unban_date(ban_minutes)
        cls.ban(chat, until_date=unban_date)
        cls.timeout_alerts = 0
        cls.send_ban_message_to_group(chat, ban_minutes)
        cls.send_private_ban_message(user, ban_minutes, unban_date)
        cls.schedule_unban_message(user, chat, ban_minutes)
        cls.increment_cioppy_bans()

    @classmethod
    def get_ban_minutes(cls):
        ban_times = Db.get().get_cioppy_bans() + 1
        return cls.increment_function(ban_times)

    @classmethod
    def increment_function(cls, k) -> int:
        return ceil(cls.initial_ban_time_in_minutes * (k ** 1.5))

    @classmethod
    def get_unban_date(cls, minutes):
        time_now = utils.os_utils.get_current_local_datetime()
        return time_now + timedelta(minutes=minutes)

    @classmethod
    def ban(cls, chat: Chat, until_date):
        try:
            success = chat.ban_member(cls.CIOPPY_USER_ID, until_date=until_date)
            if not success:
                raise CannotBanMember()
        except telegram.error.BadRequest:
            raise CannotBanMember()

    @classmethod
    def send_ban_message_to_group(cls, chat, ban_minutes):
        chat.send_message(cls.BAN_MESSAGE.format(minutes=ban_minutes))

    @classmethod
    def send_private_ban_message(cls, user, ban_minutes, unban_date):
        user.send_message(cls.BAN_PRIVATE_MESSAGE.format(minutes=ban_minutes,
                                                         date=unban_date.strftime("%d/%m"),
                                                         hour=unban_date.strftime("%H:%M")))

    @classmethod
    def schedule_unban_message(cls, user, chat: Chat, ban_minutes):
        invite_link = chat.invite_link or chat.create_invite_link(member_limit=1).invite_link
        threading.Timer(ban_minutes * 60, user.send_message, args=[
            cls.UNBAN_PRIVATE_MESSAGE.format(
                group_name=chat.title,
                link=invite_link)
        ]).start()

    @classmethod
    def increment_cioppy_bans(cls):
        number_of_bans = Db.get().get_cioppy_bans() + 1
        Db.get().set_cioppy_bans(number_of_bans)

    @classmethod
    def warn_member(cls, max_alerts, update: Update):
        update.effective_message.reply_text(
            cls.WARN_MESSAGE.format(current_warns=cls.timeout_alerts,
                                    max_warns=max_alerts)
        )

    @classmethod
    def send_error_message(cls, chat):
        chat.send_message(cls.BAN_ERROR_MESSAGE)


class CannotBanMember(Exception):
    pass
