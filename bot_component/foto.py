import random
from os import listdir

from telegram import Update
from telegram.ext import CallbackContext

insieme_fica = {"vagina", "fica", "pisella", "fregna", "figa", "utero", "vulva", "gnegna", "picchia",
                "barattolo della mostarda", "patata", "gnagna"}
insieme_tette = {"tette", "zinne", "seno"
                                   "poppe", "mammelle", "boops", "boop", "tetta", "zinna"}
insieme_pene = {"pene", "pisello", "cazzo", "cazzetto", "mazza", "bastone", "arnese", "manganello",
                "gingillo", "minchia", "lalla"}
insieme_negro = {r"neg?r\w", "nigga"}
insieme_culo = {"culo", "lato b", "ano",
                "fondoschiena", "natiche", "natica", "sedere"}


class Foto:
    @staticmethod
    def command_handler_foto(update: Update, context: CallbackContext):
        testo = str(update.effective_message.text).lower()

        if any((x in testo for x in insieme_culo)):
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=Foto.__get_random_photo("Culo"))
        if any((x in testo for x in insieme_fica)):
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=Foto.__get_random_photo("Fica"))
        if any((x in testo for x in insieme_pene)):
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=Foto.__get_random_photo("Cazzi"))
        if any((x in testo for x in insieme_tette)):
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=Foto.__get_random_photo("Tette"))

    @staticmethod
    def __get_random_photo(category: str) -> bytes:
        directory = f"./Foto/{category}/"
        random_photo = directory + random.choice(listdir(directory))
        with open(random_photo, "rb") as photo:
            return photo.read()
