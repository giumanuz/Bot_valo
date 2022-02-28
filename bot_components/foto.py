import logging
import random
import re
import threading
from os import listdir

from telegram import Update, Message
from telegram.ext import CallbackContext

from utils.os_utils import get_absolute_path

_insieme_fica = {"vagina", "fica", "pisella", "fregna", "figa", "utero", "vulva", "gnegna", "picchia",
                 "barattolo della mostarda", "patata", "gnagna"}

_insieme_tette = {"tette", "zinne", "seno", "coseno",
                  "poppe", "mammelle", "boobs", "boob", "tetta", "zinna"}

_insieme_pene = {"pene", "pisello", "cazzo", "cazzetto", "cazzone", "mazza", "bastone", "arnese", "manganello",
                 "gingillo", "minchia", "lalla"}

_insieme_culo = {"culo", "lato b", "ano", "deretano",
                 "fondoschiena", "natiche", "natica", "sedere"}


class Foto:

    removal_seconds: dict[int, float] = {}

    @classmethod
    def handle_message(cls, update: Update, context: CallbackContext):
        testo = str(update.effective_message.text).lower()
        # noinspection PyTypeChecker
        res: Message = None
        regex_pattern = r"([^\w]|^)mazza([^\w]|$)"

        if any(re.search(regex_pattern.format(y), testo) for y in _insieme_culo):
            res = context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                        photo=cls.__get_random_photo("culo"))
        elif any(re.search(regex_pattern.format(y), testo) for y in _insieme_fica):
            res = context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                        photo=cls.__get_random_photo("fica"))
        elif any(re.search(regex_pattern.format(y), testo) for y in _insieme_pene):
            res = context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                        photo=cls.__get_random_photo("cazzi"))
        elif any(re.search(regex_pattern.format(y), testo) for y in _insieme_tette):
            res = context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                        photo=cls.__get_random_photo("tette"))
        if res is not None:
            seconds = cls.removal_seconds.get(update.effective_chat.id, 5)
            threading.Timer(seconds, lambda: res.delete()).start()

    @classmethod
    def __get_random_photo(cls, category: str) -> bytes:
        directory = get_absolute_path(f"/resources/photos/{category}")
        random_photo = f"{directory}/{random.choice(listdir(directory))}"
        try:
            with open(random_photo, "rb") as photo:
                return photo.read()
        except FileNotFoundError:
            logging.warning(f"Photo '{random_photo}' not found!")
