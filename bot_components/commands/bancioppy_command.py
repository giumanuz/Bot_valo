from threading import Timer

from telegram import User, Update, Chat
from telegram.ext import Dispatcher, CommandHandler

from bot_components.anti_cioppy_policy import AntiCioppyPolicy


class BanCioppyCommand:
    CIOPPY_USER = User(id=AntiCioppyPolicy.CIOPPY_USER_ID,
                       first_name="",
                       is_bot=False)

    current_voters: dict[int, list[int]] = {}
    active_reset_timers: dict[int, Timer] = {}

    required_voters_to_ban = 4
    reset_voters_after_seconds = 200

    VOTANTS_MESSAGE = f"Hai votato per bannare cioppy! Voti {{cur_voters}} su {required_voters_to_ban}"

    @classmethod
    def init(cls, dispatcher: Dispatcher):
        dispatcher.add_handler(CommandHandler("banCioppy", cls.ban_cioppy, run_async=True))
        cls.CIOPPY_USER.bot = dispatcher.bot

    @classmethod
    def ban_cioppy(cls, update: Update, _):
        print("gel")
        chat = update.effective_chat
        user_id = update.effective_user.id
        current_voters_on_chat = cls.current_voters.setdefault(chat.id, [])
        if user_id in current_voters_on_chat:
            return
        current_voters_on_chat.append(user_id)
        if len(current_voters_on_chat) >= cls.required_voters_to_ban:
            AntiCioppyPolicy.try_to_timeout_member(chat, cls.CIOPPY_USER)
            cls.stop_chat_timer(chat.id)
            cls.current_voters.pop(chat.id)
        else:
            cls.send_current_voters_message(chat)
            cls.restart_timer(chat.id)

    @classmethod
    def stop_chat_timer(cls, chat_id):
        if chat_id in cls.active_reset_timers:
            timer = cls.active_reset_timers[chat_id]
            if timer and timer.is_alive():
                timer.cancel()

    @classmethod
    def send_current_voters_message(cls, chat: Chat):
        message = cls.VOTANTS_MESSAGE.format(
            cur_voters=len(cls.current_voters[chat.id])
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
