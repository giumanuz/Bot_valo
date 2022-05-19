from telegram import Update, ChatMemberAdministrator, ChatMemberOwner
from telegram.ext import Dispatcher, CommandHandler

from bot_components.undo.fixed_stack import FixedStack
from bot_components.undo.state_change import StateChange


class UndoSequence:
    MAX_UNDOS = 5
    # TODO: make chat-specific
    state_stack = FixedStack[StateChange](MAX_UNDOS)

    ERROR_MESSAGE_ADMIN = "Per annullare l'azione è necessario un amministratore"
    ERROR_MESSAGE_LIMIT_REACHED = f"Non puoi annullare più di {MAX_UNDOS} azioni!"
    ERROR_MESSAGE_GENERIC = "C'è stato un errore nell'annullamento dell'azione"

    @classmethod
    def init(cls, dispatcher: Dispatcher):
        dispatcher.add_handler(CommandHandler("undo", cls.undo_interface, run_async=True))

    @classmethod
    def undo_interface(cls, update: Update, _):
        chat = update.effective_chat
        if cls.undo_requires_admin():
            chat_member = chat.get_member(update.effective_user.id)
            if not cls.has_admin_rights(chat_member):
                chat.send_message(cls.ERROR_MESSAGE_ADMIN)
                return
        try:
            cls.undo_latest_action()
        except CannotUndoAnymore:
            chat.send_message(cls.ERROR_MESSAGE_LIMIT_REACHED)
        except ActionNotUndoable:
            chat.send_message(cls.ERROR_MESSAGE_GENERIC)

    @classmethod
    def has_admin_rights(cls, chat_member):
        return isinstance(chat_member, ChatMemberAdministrator) \
               or isinstance(chat_member, ChatMemberOwner)

    @classmethod
    def undo_latest_action(cls):
        if cls.state_stack.is_empty():
            raise CannotUndoAnymore()
        state = cls.state_stack.pop()
        if not state.can_undo:
            raise ActionNotUndoable()
        cls._try_to_undo(state)

    @classmethod
    def _try_to_undo(cls, state):
        try:
            state.undo()
        except Exception as e:
            cls.state_stack.push(state)
            raise UndoError(e)

    @classmethod
    def undo_requires_admin(cls):
        return cls.state_stack.last().requires_admin

    @classmethod
    def register_action(cls, action: StateChange):
        cls.state_stack.push(action)


class CannotUndoAnymore(Exception):
    pass


class ActionNotUndoable(Exception):
    pass


class UndoError(Exception):
    _error: Exception

    def __init__(self, error: Exception = None):
        super().__init__()
        self._error = error

    @property
    def error(self):
        return self._error

    def __repr__(self):
        return self._error.__repr__()
