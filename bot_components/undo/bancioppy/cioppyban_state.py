from telegram import Chat

from bot_components.anti_cioppy_policy import AntiCioppyPolicy as Acp
from bot_components.commands.bancioppy_command import BanCioppyCommand
from bot_components.db.db_manager import Database
from bot_components.undo.state_change import StateChange


class CioppyBanState(StateChange):
    def __init__(self, chat: Chat):
        self.chat = chat

    @property
    def requires_admin(self) -> bool:
        return True

    @property
    def can_undo(self) -> bool:
        return True

    def undo(self):
        if BanCioppyCommand.cioppy_is_in_chat(self.chat):
            raise CioppyAlreadyInChat()
        self.chat.unban_member(Acp.CIOPPY_USER_ID)
        timer = Acp.active_timers.pop(self.chat.id, None)
        if timer and timer.is_alive():
            timer.cancel()
        Acp.send_unban_message(self.chat)
        self.undo_ban_from_db()
        self.reset_chat_voters()

    @classmethod
    def undo_ban_from_db(cls):
        db = Database.get()
        bans = db.get_cioppy_bans()
        restored_bans = max(0, bans - 1)
        db.set_cioppy_bans(restored_bans)

    def reset_chat_voters(self):
        BanCioppyCommand.current_voters.pop(self.chat.id, None)


class CioppyAlreadyInChat(Exception):
    pass
