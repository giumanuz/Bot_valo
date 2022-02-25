import json
import logging
from datetime import datetime
from re import search

from pytz import utc, timezone
from telegram import Update
from telegram.ext import CallbackContext, Dispatcher, MessageHandler, Filters

from bot_components.foto import Foto
from bot_components.insulti import Insulti
from bot_components.risposte import Risposte
from bot_components.utils.os_utils import path_to_text_file

week_codes = {0: "monday", 1: "tuesday", 2: "wednesday", 3: "thursday", 4: "friday", 5: "saturday", 6: "sunday"}
blacklisted_hours: dict[str, list[int]] = None


def add_message_handlers(dispatcher: Dispatcher):
    init_hour_blacklist()
    dispatcher.add_handler(MessageHandler(
        Filters.text, _inoltra_messaggio, pass_user_data=True, run_async=True))


def init_hour_blacklist():
    try:
        with open(path_to_text_file("schedule_blacklist.json"), "r") as f:
            global blacklisted_hours
            blacklisted_hours = json.load(f)
    except OSError:
        logging.warning("Errore nell'apertura del file 'schedule_blacklist.json'. "
                        "Sicuro che si trova in /resources/text_files/?")


def _inoltra_messaggio(update: Update, context: CallbackContext):
    if "botvalo timer" in update.effective_message.text.lower():
        set_Foto_delete_timer(update, context)
    Risposte.handle_message(update, context)
    Insulti.handle_message(update, context)
    if not hour_in_blacklist():
        Foto.handle_message(update, context)


def set_Foto_delete_timer(update, context: CallbackContext):
    try:
        seconds = search(r"\d+(.\d+)?", update.effective_message.text).group(0)
        Foto.removal_seconds[update.effective_chat.id] = float(seconds)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f"Le foto verranno eliminate dopo {seconds} secondi")
    except TypeError:
        pass


def hour_in_blacklist() -> bool:
    if blacklisted_hours is None:
        return False
    local_now = get_now_datetime_local()
    today_weekday_code = local_now.weekday()
    today_as_weekday_str = week_codes[today_weekday_code]
    if today_as_weekday_str not in blacklisted_hours:
        return False
    forbidden_hour_interval = blacklisted_hours[today_as_weekday_str]
    return forbidden_hour_interval[0] <= local_now.hour < forbidden_hour_interval[1]


def get_now_datetime_local():
    time_now_utc = datetime.utcnow()
    local_timezone = timezone("Europe/Rome")
    return utc.localize(time_now_utc).astimezone(local_timezone)
