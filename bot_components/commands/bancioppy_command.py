import random
from datetime import datetime
from threading import Timer

import telegram
from telegram import User, Update, Chat
from telegram.ext import Dispatcher, CommandHandler

from bot_components.anti_cioppy_policy import AntiCioppyPolicy as Acp
from bot_components.commands_registration import CommandRegister
from bot_components.db.db_manager import Database


class BanCioppyCommand:
    CIOPPY_USER = User(id=Acp.CIOPPY_USER_ID,
                       first_name="",
                       is_bot=False)

    current_voters: dict[int, set[int]] = {}
    active_reset_timers: dict[int, Timer] = {}

    required_voters_to_ban = 4
    reset_voters_after_seconds = 720

    VOTANTS_MESSAGE = "Hai votato per bannare cioppy! Voti {cur_voters} su {min_voters}"
    GIFT_VOTE_MESSAGE = "Vi regalo un voto dai, oggi cioppy mi sta sul cazzo"
    GIFT_PROBABILITY = 0.08

    _random: random.Random

    @classmethod
    def init(cls, dispatcher: Dispatcher):
        dispatcher.add_handler(CommandHandler("banCioppy", cls.vote_for_cioppy_ban, run_async=True))
        Database.get().register_for_config_changes("timeout", cls.update_required_votants_to_ban)
        cls.CIOPPY_USER.bot = dispatcher.bot
        CommandRegister.register_command("bancioppy", "Vota per bannare Cioppy dal gruppo, se presente.")
        cls._random = random.Random(datetime.utcnow().timestamp())

    @classmethod
    def update_required_votants_to_ban(cls):
        new_required_votants = Database.get().get_minimum_voters_required_to_ban_cioppy()
        cls.required_voters_to_ban = new_required_votants

    @classmethod
    def vote_for_cioppy_ban(cls, update: Update, _):
        chat = update.effective_chat
        if not cls.cioppy_is_in_chat(chat):
            return
        user_id = update.effective_user.id
        current_voters_on_chat = cls.current_voters.setdefault(chat.id, set())
        if user_id in current_voters_on_chat:
            return
        current_voters_on_chat.add(user_id)
        cls.send_current_voters_message(chat)
        cls.add_gift_ban_with_probability(chat)
        if len(cls.current_voters[chat.id]) >= cls.required_voters_to_ban:
            cls.ban_cioppy_and_reset_voters(chat)
        else:
            cls.restart_timer(chat.id)

    @classmethod
    def cioppy_is_in_chat(cls, chat: Chat) -> bool:
        try:
            m = chat.get_member(Acp.CIOPPY_USER_ID)
            if not m:
                return False
            match m.status:
                case (m.LEFT | m.KICKED):
                    return False
                case _:
                    return True
        except telegram.TelegramError:
            return False

    @classmethod
    def add_gift_ban_with_probability(cls, chat):
        if cls.current_voters[chat.id] == cls.required_voters_to_ban - 1 and random.random() < cls.GIFT_PROBABILITY:
            cls.current_voters[chat.id].add(-1)
            chat.send_message(cls.GIFT_VOTE_MESSAGE)

    @classmethod
    def ban_cioppy_and_reset_voters(cls, chat):
        Acp.try_to_timeout_member(chat, cls.CIOPPY_USER)
        cls.stop_chat_timer(chat.id)
        cls.reset_voters(chat.id)

    @classmethod
    def stop_chat_timer(cls, chat_id):
        if chat_id in cls.active_reset_timers:
            timer = cls.active_reset_timers[chat_id]
            if timer and timer.is_alive():
                timer.cancel()

    @classmethod
    def send_current_voters_message(cls, chat: Chat):
        message = cls.VOTANTS_MESSAGE.format(
            cur_voters=len(cls.current_voters[chat.id]),
            min_voters=cls.required_voters_to_ban
        )
        chat.send_message(message)

    @classmethod
    def restart_timer(cls, chat_id):
        cls.stop_chat_timer(chat_id)
        new_timer = Timer(cls.reset_voters_after_seconds,
                          cls.reset_voters,
                          [chat_id])
        new_timer.start()
        cls.active_reset_timers[chat_id] = new_timer

    @classmethod
    def reset_voters(cls, chat_id):
        if chat_id in cls.current_voters:
            cls.current_voters.pop(chat_id, None)
