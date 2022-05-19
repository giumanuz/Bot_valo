from threading import Timer

import telegram
from telegram import Update, Chat
from telegram.ext import Dispatcher, CommandHandler

from bot_components.anti_cioppy_policy import AntiCioppyPolicy as Acp
from bot_components.db.db_manager import Database
from bot_components.undo.undo import UndoSequence


class BanCioppyCommand:
    current_voters: dict[int, set[int]] = {}
    active_reset_timers: dict[int, Timer] = {}

    required_voters_to_ban = 4
    reset_voters_after_seconds = 200

    VOTANTS_MESSAGE = "Hai votato per bannare cioppy! Voti {cur_voters} su {min_voters}"
    REVOKED_VOTE_MESSAGE = "Hai ritirato il tuo voto! Ora i voti sono {cur_voters} su {min_voters}"

    @classmethod
    def init(cls, dispatcher: Dispatcher):
        dispatcher.add_handler(CommandHandler("banCioppy", cls.ban_cioppy, run_async=True))
        Database.get().register_for_config_changes("timeout", cls.update_required_votants_to_ban)

    @classmethod
    def update_required_votants_to_ban(cls):
        new_required_votants = Database.get().get_minimum_voters_required_to_ban_cioppy()
        cls.required_voters_to_ban = new_required_votants

    @classmethod
    def ban_cioppy(cls, update: Update, _):
        chat = update.effective_chat
        if not cls.cioppy_is_in_chat(chat):
            return
        user_id = update.effective_user.id
        current_voters_on_chat = cls.current_voters.setdefault(chat.id, set())
        if user_id in current_voters_on_chat:
            return
        current_voters_on_chat.add(user_id)
        cls.register_action_for_undo(chat, user_id)
        if len(cls.current_voters[chat.id]) >= cls.required_voters_to_ban:
            Acp.try_to_timeout_member(chat)
            cls.stop_chat_timer(chat.id)
            cls.reset_voters(chat.id)
        else:
            cls.send_current_voters_message(chat)
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
    def register_action_for_undo(cls, chat: Chat, voter_id: int):
        from bot_components.undo.bancioppy.bancioppy_vote_state import BanCioppyVoteState
        action = BanCioppyVoteState(chat, voter_id)
        UndoSequence.register_action(action)

    @classmethod
    def stop_chat_timer(cls, chat_id):
        if chat_id in cls.active_reset_timers:
            timer = cls.active_reset_timers[chat_id]
            if timer and timer.is_alive():
                timer.cancel()

    @classmethod
    def send_current_voters_message(cls, chat: Chat):
        message = cls.format_voters_message(cls.VOTANTS_MESSAGE, chat.id)
        chat.send_message(message)

    @classmethod
    def send_revoked_vote_message(cls, chat: Chat):
        message = cls.format_voters_message(cls.REVOKED_VOTE_MESSAGE, chat.id)
        chat.send_message(message)

    @classmethod
    def format_voters_message(cls, message: str, chat_id):
        return message.format(
            cur_voters=len(cls.current_voters[chat_id]),
            min_voters=cls.required_voters_to_ban
        )

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
