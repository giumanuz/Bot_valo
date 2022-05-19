from telegram import Chat

from bot_components.commands.bancioppy_command import BanCioppyCommand
from bot_components.undo.state_change import StateChange


class BanCioppyVoteState(StateChange):
    def __init__(self, chat: Chat, voter_id: int):
        self.chat = chat
        self.voter_id = voter_id

    @property
    def requires_admin(self) -> bool:
        return False

    @property
    def can_undo(self) -> bool:
        return True

    def undo(self):
        BanCioppyCommand.current_voters[self.chat.id].remove(self.voter_id)
        BanCioppyCommand.send_revoked_vote_message(self.chat)
