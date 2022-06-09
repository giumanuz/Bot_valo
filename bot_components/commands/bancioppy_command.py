import random
import threading
from datetime import datetime, timedelta
from threading import Timer

import telegram
from telegram import User, Update, Chat
from telegram.ext import Dispatcher, CommandHandler

from bot_components.anti_cioppy_policy import AntiCioppyPolicy as Acp, CannotBanMember
from bot_components.commands_registration import CommandRegister
from bot_components.db.db_manager import Database
from utils.os_utils import get_current_local_datetime


class BanCioppyCommand:
    CIOPPY_USER = User(id=Acp.CIOPPY_USER_ID,
                       first_name="",
                       is_bot=False)

    current_voters: dict[int, list[User]] = {}
    active_reset_timers: dict[int, Timer] = {}

    required_voters_to_ban = 4
    reset_voters_after_seconds = 720

    VOTANTS_MESSAGE = "Hai votato per bannare cioppy! Voti {cur_voters} su {min_voters}"
    GIFT_VOTE_MESSAGE = "Vi regalo un voto dai, oggi cioppy mi sta sul cazzo"
    GIFT_PROBABILITY = 0.08

    TWIST_PROBABILITY = 1.00  # TODO: change probability

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
        user = update.effective_user
        current_voters_on_chat = cls.current_voters.setdefault(chat.id, [])
        if user in current_voters_on_chat:
            return
        current_voters_on_chat.append(user)
        cls.send_current_voters_message(chat)
        cls.add_gift_ban_with_probability(chat)
        if len(cls.current_voters[chat.id]) >= 1:  # cls.required_voters_to_ban:
            if cls.is_twist() and cls.required_voters_to_ban >= 6:
                cls.twist(chat)
            else:
                cls.ban_user_and_reset_voters(chat, cls.CIOPPY_USER)
        else:
            cls.restart_timer(chat.id)

    @classmethod
    def is_twist(cls):
        return random.random() < cls.TWIST_PROBABILITY

    @classmethod
    def twist(cls, chat: Chat):
        chat.send_message("Twist! Mo viene bannato uno dei votanti!")
        dice_value = chat.send_dice(emoji=telegram.constants.DICE_DICE).dice.value
        user_to_ban = cls.current_voters[chat.id][dice_value - 1]
        cls.stop_chat_timer(chat.id)
        cls.reset_voters(chat.id)
        threading.Timer(10, cls.twist_ban_and_send_message, [chat, user_to_ban]).start()

    @classmethod
    def twist_ban_and_send_message(cls, chat: Chat, user):
        if cls.user_is_admin(chat, user):
            chat.send_message("Purtroppo il malcapitato è un admin, sarà per la prossima!")
            return

        time_now = get_current_local_datetime()
        unban_date = time_now + timedelta(minutes=20)
        try:
            chat.send_message(f"Eh eh eh, addio {user}!")
            Acp.ban_user(user, chat, unban_date)
        except CannotBanMember:
            chat.send_message("E invece ti è andata bene, a quanto pare non posso bannarti!")

    @classmethod
    def user_is_admin(cls, chat: Chat, user: User) -> bool:
        chat_admins = chat.get_administrators()
        return user in (member.user for member in chat_admins)

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
        if cls.current_voters[chat.id] == cls.required_voters_to_ban - 1 \
                and random.random() < cls.GIFT_PROBABILITY:
            cls.current_voters[chat.id].append(-1)
            chat.send_message(cls.GIFT_VOTE_MESSAGE)

    @classmethod
    def ban_user_and_reset_voters(cls, chat, user):
        Acp.try_to_timeout_member(chat, user)
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
