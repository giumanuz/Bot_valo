import datetime
import json
import logging

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
    Risposte.handle_message(update, context)
    Insulti.handle_message(update, context)
    if not hour_in_blacklist():
        Foto.handle_message(update, context)


def hour_in_blacklist() -> bool:
    if blacklisted_hours is None:
        return False
    today_as_weekday = datetime.datetime.now().weekday()
    weekday_int_code = week_codes[today_as_weekday]
    forbidden_hour_interval = blacklisted_hours[weekday_int_code]
    hour_now = datetime.datetime.now().hour
    return forbidden_hour_interval[0] <= hour_now < forbidden_hour_interval[1]
