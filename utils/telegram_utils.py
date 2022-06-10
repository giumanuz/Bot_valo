from datetime import timedelta

from telegram import User, Chat
from telegram.error import BadRequest

from utils.os_utils import get_current_local_datetime


def get_effective_text(update):
    """Restituisce il testo effettivo del messaggio
    contenuto in `update`."""
    if update.effective_message.caption is not None:
        return str(update.effective_message.caption).lower()
    elif update.effective_message.text is not None:
        return str(update.effective_message.text).lower()


def ban_user(user: User, chat: Chat, *, days=0, minutes=0, seconds=0):
    """Banna l'utente `user` dalla chat `chat`.
    In caso di fallimento, lancia `CannotBanMember`."""
    time_now = get_current_local_datetime()
    until_date = time_now + timedelta(days=days,
                                      minutes=minutes,
                                      seconds=seconds)
    try:
        success = chat.ban_member(user.id, until_date=until_date)
        if not success:
            raise CannotBanMember()
    except BadRequest:
        raise CannotBanMember()


def get_unban_date(minutes):
    time_now = get_current_local_datetime()
    return time_now + timedelta(minutes=minutes)


class CannotBanMember(Exception):
    pass
