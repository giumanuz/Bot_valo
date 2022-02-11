import logging
import random
from os import listdir, path

from telegram import Update
from telegram.ext import CallbackContext

_insieme_fica = {"vagina", "fica", "pisella", "fregna", "figa", "utero", "vulva", "gnegna", "picchia",
                 "barattolo della mostarda", "patata", "gnagna"}
_insieme_tette = {"tette", "zinne", "seno",
                  "poppe", "mammelle", "boobs", "boob", "tetta", "zinna"}
_insieme_pene = {"pene", "pisello", "cazzo", "cazzetto", "mazza", "bastone", "arnese", "manganello",
                 "gingillo", "minchia", "lalla"}
_insieme_culo = {"culo", "lato b", "ano",
                 "fondoschiena", "natiche", "natica", "sedere"}


def get_set_list():
    yield _insieme_culo
    yield _insieme_tette
    yield _insieme_pene
    yield _insieme_fica


class Foto:
    @classmethod
    def handle_message(cls, update: Update, context: CallbackContext):
        testo = str(update.effective_message.text).lower()

        if testo in _insieme_culo:
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=cls.__get_random_photo("culo"))
        elif testo in _insieme_fica:
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=cls.__get_random_photo("fica"))
        elif testo in _insieme_pene:
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=cls.__get_random_photo("cazzi"))
        elif testo in _insieme_tette:
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=cls.__get_random_photo("tette"))

    @classmethod
    def __get_random_photo(cls, category: str) -> bytes:
        directory = path.join(
            path.dirname(__file__),
            "..", "resources", "photos", category
        )
        random_photo = f"{directory}/{random.choice(listdir(directory))}"
        try:
            with open(random_photo, "rb") as photo:
                return photo.read()
        except FileNotFoundError:
            logging.warning(f"Photo '{random_photo}' not found!")
