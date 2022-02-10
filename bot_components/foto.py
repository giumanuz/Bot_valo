import logging
import random
from os import listdir

from telegram import Update
from telegram.ext import CallbackContext

insieme_fica = {"vagina", "fica", "pisella", "fregna", "figa", "utero", "vulva", "gnegna", "picchia",
                "barattolo della mostarda", "patata", "gnagna"}
insieme_tette = {"tette", "zinne", "seno",
                 "poppe", "mammelle", "boobs", "boob", "tetta", "zinna"}
insieme_pene = {"pene", "pisello", "cazzo", "cazzetto", "mazza", "bastone", "arnese", "manganello",
                "gingillo", "minchia", "lalla"}
insieme_culo = {"culo", "lato b", "ano",
                "fondoschiena", "natiche", "natica", "sedere"}


class Foto:
    @classmethod
    def command_handler_foto(cls, update: Update, context: CallbackContext):
        testo = str(update.effective_message.text).lower()

        if testo in insieme_culo:
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=cls.__get_random_photo("culo"))
        elif testo in insieme_fica:
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=cls.__get_random_photo("fica"))
        elif testo in insieme_pene:
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=cls.__get_random_photo("cazzi"))
        elif testo in insieme_tette:
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=cls.__get_random_photo("tette"))

    @classmethod
    def __get_random_photo(cls, category: str) -> bytes:
        directory = f"./resources/photos/{category}/"
        random_photo = directory + random.choice(listdir(directory))
        try:
            with open(random_photo, "rb") as photo:
                return photo.read()
        except FileNotFoundError:
            logging.warning(f"Photo '{random_photo}' not found!")
