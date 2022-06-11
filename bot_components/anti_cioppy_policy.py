from datetime import datetime, timedelta
from math import ceil

import telegram.error
from telegram import Chat, Update, User

import utils.os_utils
from bot_components.db.db_manager import Database as Db


class AntiCioppyPolicy:
    CIOPPY_USER_ID = 364369396

    BAN_MESSAGE = "Bannato cioppy per {minutes} minuti!"
    BAN_ERROR_MESSAGE = "Non sono riuscito a bannare quel troione di cioppy. Forse mi mancano dei permessi?"
    WARN_MESSAGE = "E basta co' sti discorsi! Avvertimento {current_warns} di {max_warns}, e poi ti banno!"
    SINGLE_WARN_MESSAGE = "E basta co' sti discorsi! Alla prossima ti banno!"

    BAN_PRIVATE_MESSAGE = "Sei stato bannato per {minutes} minuti per aver fatto discorsi del cazzo," \
                          " come al solito\\. Sarai sbannato il {date} alle {hour}\\." \
                          " Potrai usare [questo link]({link}) per rientrare\\."

    DECREASE_BANS_AFTER_DAYS = 2

    timeout_words_list = []
    initial_ban_time_in_minutes: int = 8  # must be >= 1

    timeout_alerts = 0

    @classmethod
    def init(cls):
        Db.get().register_for_config_changes("timeout", cls._init_timeout_words_list)

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
    def contains_a_timeout_word(cls, text: str):
        adjusted_text = cls.adjust_text(text)
        return any(cls.has_algorithm(adjusted_text, e) for e in cls.timeout_words_list)

    @classmethod
    def adjust_text(cls, text: str) -> str:
        text = text.replace("1", "i") \
            .replace("!", "i") \
            .replace("2", "z") \
            .replace("3", "e") \
            .replace("4", "a") \
            .replace("@", "a") \
            .replace("$", "s") \
            .replace("5", "s") \
            .replace("7", "t") \
            .replace("8", "b") \
            .replace("k", "c") \
            .replace("0", "o")
        text = ''.join(s for s in text if s.isalnum())
        return text

    @classmethod
    def has_algorithm(cls, text: str, word: str):
        reduced_text = ''.join(c for c in text if c not in 'uaoie ')
        reduced_word = ''.join(c for c in word if c not in 'uaoie ')
        return reduced_word in reduced_text

    @classmethod
    def try_to_timeout_member(cls, chat: Chat, user: User):
        try:
            cls._timeout_member(chat, user)
        except CannotBanMember:
            cls.send_error_message(chat)

    @classmethod
    def _timeout_member(cls, chat, user):
        cls.decrease_ban_count_if_necessary()
        ban_minutes = cls.get_ban_minutes()
        unban_date = cls.get_unban_date(ban_minutes)
        cls.ban_user(user.id, chat, until_date=unban_date)
        cls.timeout_alerts = 0
        cls.send_ban_message_to_group(chat, ban_minutes)
        cls.send_private_ban_message(chat, user, ban_minutes, unban_date)
        cls.increment_cioppy_bans()

    @classmethod
    def get_ban_minutes(cls):
        ban_times = Db.get().get_cioppy_bans() + 1
        return cls.increment_function(ban_times)

    @classmethod
    def decrease_ban_count_if_necessary(cls):
        db = Db.get()
        last_ban_reset = datetime.fromtimestamp(db.get_cioppy_decrease_ban_timestamp())
        elapsed_time = datetime.utcnow() - last_ban_reset
        bans_to_remove = elapsed_time.days // cls.DECREASE_BANS_AFTER_DAYS
        if bans_to_remove == 0:
            return
        current_bans_count = db.get_cioppy_bans()
        new_ban_count = max(0, current_bans_count - bans_to_remove)
        db.set_cioppy_bans(new_ban_count)
        db.set_cioppy_decrease_ban_timestamp(datetime.utcnow().timestamp())

    @classmethod
    def increment_function(cls, k) -> int:
        return ceil(cls.initial_ban_time_in_minutes * (k ** 1.5))

    @classmethod
    def get_unban_date(cls, minutes):
        time_now = utils.os_utils.get_current_local_datetime()
        return time_now + timedelta(minutes=minutes)

    @classmethod
    def ban_user(cls, user: User, chat: Chat, until_date):
        try:
            success = chat.ban_member(user.id, until_date=until_date)
            if not success:
                raise CannotBanMember()
        except telegram.error.BadRequest:
            raise CannotBanMember()

    @classmethod
    def send_ban_message_to_group(cls, chat, ban_minutes):
        chat.send_message(cls.BAN_MESSAGE.format(minutes=ban_minutes))

    @classmethod
    def send_private_ban_message(cls, chat, user, ban_minutes, unban_date):
        invite_link = chat.invite_link or chat.create_invite_link(member_limit=1).invite_link
        user.send_message(cls.BAN_PRIVATE_MESSAGE
                          .format(minutes=ban_minutes,
                                  date=unban_date.strftime("%dice/%m"),
                                  hour=unban_date.strftime("%H:%M"),
                                  link=invite_link),
                          parse_mode=telegram.parsemode.ParseMode.MARKDOWN_V2)

    @classmethod
    def increment_cioppy_bans(cls):
        number_of_bans = Db.get().get_cioppy_bans() + 1
        Db.get().set_cioppy_bans(number_of_bans)

    @classmethod
    def warn_member(cls, max_alerts, update: Update):
        message = cls.SINGLE_WARN_MESSAGE if max_alerts == 1 else cls.WARN_MESSAGE
        update.effective_message.reply_text(
            message.format(current_warns=cls.timeout_alerts,
                           max_warns=max_alerts)
        )

    @classmethod
    def send_error_message(cls, chat):
        chat.send_message(cls.BAN_ERROR_MESSAGE)


class CannotBanMember(Exception):
    pass
