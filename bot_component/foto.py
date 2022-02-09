import random
from telegram import Update
from telegram.ext import MessageHandler, Filters, CallbackContext
from os import listdir

insieme_fica = {"vagina", "fica", "pisella", "fregna", "figa", "utero", "vulva", "gnegna", "picchia",
                "barattolo della mostarda", "patata", "gnagna"}
insieme_tette = {"tette", "zinne", "seno"
                 "poppe", "mammelle", "boops", "boop", "tetta", "zinna"}
insieme_pene = {"pene", "pisello", "cazzo", "cazzetto", "mazza", "bastone", "arnese", "manganello",
                "gingillo", "minchia", "lalla"}
insieme_negro = {r"neg?r\w", "nigga"}
insieme_culo = {"culo", "lato ?b", "deretano",
                "fondoschiena", "natiche", "natica", "sedere"}
class Foto:

    @staticmethod
    def command_handler_foto(self, update: Update, context: CallbackContext):
        testo = str(update.effective_message.text).lower()

        if any([x in testo for x in insieme_culo]):
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=open("./Foto/Culo/" + random.choice(self.__lista_culo), "rb").read())
        if any([x in testo for x in insieme_fica]):
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=open("./Foto/Fica/" + random.choice(self.__lista_fica), "rb").read())
        if any([x in testo for x in insieme_pene]):
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=open("./Foto/Cazzi/" + random.choice(self.__lista_cazzi), "rb").read())
        if any([x in testo for x in insieme_tette]):
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=open("./Foto/Tette/" + random.choice(self.__lista_tette), "rb").read())

    @staticmethod
    def __get_random_photo(category):
        dir = f"./Foto/{category}/"
        random_photo = dir + random.choice(listdir(directory))
        open(directory + , "rb").read()

def init_foto(dispatcher):

    dispatcher.add_handler(MessageHandler(
        Filters.text, Foto.command_handler_foto, pass_user_data=True, run_async=True))
