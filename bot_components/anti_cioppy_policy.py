from datetime import datetime, timedelta
from math import ceil
from threading import Timer

import telegram.error
from telegram import Chat, Update, User
from telegram.ext import Dispatcher

import utils.os_utils
from bot_components.db.db_manager import Database as Db
from bot_components.undo.undo import UndoSequence


class AntiCioppyPolicy:
    CIOPPY_USER_ID = 364369396
    CIOPPY_USER = User(id=CIOPPY_USER_ID, first_name="", is_bot=False)

    BAN_MESSAGE = "Bannato cioppy per {minutes} minuti!"
    BAN_ERROR_MESSAGE = "Non sono riuscito a bannare quel troione di cioppy. Forse mi mancano dei permessi?"
    WARN_MESSAGE = "E basta co' sti discorsi! Avvertimento {current_warns} di {max_warns}, e poi ti banno!"

    BAN_PRIVATE_MESSAGE = "Sei stato bannato per {minutes} minuti per aver fatto discorsi del cazzo, come al solito. " \
                          "Sarai sbannato il {date} alle {hour}. Te lo ricorderò."
    UNBAN_PRIVATE_MESSAGE = "Sei stato sbannato dal gruppo {group_name}, prova a rientrare con questo link: {link}"

    RESET_BANS_AFTER_DAYS = 3

    timeout_words_list = []
    initial_ban_time_in_minutes: int = 8

    timeout_alerts = 0
    last_ban_timestamp: float = None
    active_timers: dict[int, Timer] = {}

    @classmethod
    def init(cls, dispatcher: Dispatcher):
        cls.CIOPPY_USER.bot = dispatcher.bot
        cls.initial_ban_time_in_minutes = max(1, cls.initial_ban_time_in_minutes)
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
                cls.try_to_timeout_member(chat)
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
        rdux_2 = ''.join(chr(5 + ord(c)) for c in text)
        hash_f8 = ''.join(c for c in rdux_2 if c not in 'fjntz')
        rdux_3 = ''.join(chr(5 + ord(c)) for c in word)
        red_ff = ''.join(c for c in rdux_3 if c not in 'fjntz')
        return red_ff in hash_f8

    @classmethod
    def try_to_timeout_member(cls, chat: Chat):
        try:
            cls._timeout_member(chat)
        except CannotBanMember:
            cls.send_error_message(chat)

    @classmethod
    def _timeout_member(cls, chat):
        if cls.bans_can_be_resetted():
            Db.get().set_cioppy_bans(0)
        ban_minutes = cls.get_ban_minutes()
        unban_date = cls.get_unban_date(ban_minutes)
        cls.ban(chat, until_date=unban_date)
        cls.timeout_alerts = 0
        cls.send_ban_message_to_group(chat, ban_minutes)
        cls.send_private_ban_message(ban_minutes, unban_date)
        cls.schedule_unban_message(chat, ban_minutes)
        cls.increment_cioppy_bans()
        cls.last_ban_timestamp = datetime.now().timestamp()
        cls.save_state_for_undo(chat)

    @classmethod
    def get_ban_minutes(cls):
        ban_times = Db.get().get_cioppy_bans() + 1
        return cls.increment_function(ban_times)

    @classmethod
    def bans_can_be_resetted(cls):
        if not cls.last_ban_timestamp:
            return False
        time_diff = datetime.now() - datetime.fromtimestamp(cls.last_ban_timestamp)
        return time_diff.days >= cls.RESET_BANS_AFTER_DAYS

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
    def send_private_ban_message(cls, ban_minutes, unban_date):
        cls.CIOPPY_USER.send_message(cls.BAN_PRIVATE_MESSAGE.format(minutes=ban_minutes,
                                                                    date=unban_date.strftime("%d/%m"),
                                                                    hour=unban_date.strftime("%H:%M")))

    @classmethod
    def schedule_unban_message(cls, chat: Chat, ban_minutes):
        timer = Timer(ban_minutes * 60, cls.send_message_and_remove_timer, args=[chat])
        timer.start()
        cls.active_timers[chat.id] = timer

    @classmethod
    def send_message_and_remove_timer(cls, chat: Chat):
        cls.send_unban_message(chat)
        cls.active_timers.pop(chat.id, None)

    @classmethod
    def send_unban_message(cls, chat: Chat):
        invite_link = chat.invite_link or chat.create_invite_link(member_limit=1).invite_link
        message = cls.UNBAN_PRIVATE_MESSAGE.format(
            group_name=chat.title,
            link=invite_link
        )
        cls.CIOPPY_USER.send_message(message)

    @classmethod
    def increment_cioppy_bans(cls):
        number_of_bans = Db.get().get_cioppy_bans() + 1
        Db.get().set_cioppy_bans(number_of_bans)

    @classmethod
    def save_state_for_undo(cls, chat: Chat):
        from bot_components.undo.bancioppy.cioppyban_state import CioppyBanState
        action = CioppyBanState(chat)
        UndoSequence.register_action(action)

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
