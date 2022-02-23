import logging
import random
from os import listdir

from telegram import Update
from telegram.ext import CallbackContext

from bot_components.utils.os_utils import get_absolute_path

_insieme_fica = {"vagina", "fica", "pisella", "fregna", "figa", "utero", "vulva", "gnegna", "picchia",
                 "barattolo della mostarda", "patata", "gnagna"}

_insieme_tette = {"tette", "zinne", "seno", "coseno",
                  "poppe", "mammelle", "boobs", "boob", "tetta", "zinna"}

_insieme_pene = {"pene", "pisello", "cazzo", "cazzetto", "cazzone", "mazza", "bastone", "arnese", "manganello",
                 "gingillo", "minchia", "lalla"}

_insieme_culo = {"culo", "lato b", "ano", "deretano",
                 "fondoschiena", "natiche", "natica", "sedere"}


class Foto:
    @classmethod
    def handle_message(cls, update: Update, context: CallbackContext):
        testo = str(update.effective_message.text).lower()
        parole = testo.split()

        if any(x == y for x in parole for y in _insieme_culo):
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=cls.__get_random_photo("culo"))
        elif any(x == y for x in parole for y in _insieme_fica):
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=cls.__get_random_photo("fica"))
        elif any(x == y for x in parole for y in _insieme_pene):
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=cls.__get_random_photo("cazzi"))
        elif any(x == y for x in parole for y in _insieme_tette):
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=cls.__get_random_photo("tette"))

    @classmethod
    def __get_random_photo(cls, category: str) -> bytes:
        directory = get_absolute_path(f"/resources/photos/{category}")
        random_photo = f"{directory}/{random.choice(listdir(directory))}"
        try:
            with open(random_photo, "rb") as photo:
                return photo.read()
        except FileNotFoundError:
            logging.warning(f"Photo '{random_photo}' not found!")
