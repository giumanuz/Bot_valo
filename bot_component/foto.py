import random
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext, Dispatcher

insieme_fica = {"vagina", "fica", "pisella", "fregna", "figa", "utero", "vulva", "gnegna", "picchia",
                "barattolo della mostarda", "patata", "gnagna"}
insieme_tette = {"tette", "zinne", "seno", "coseno",
                 "poppe", "mammelle", "boops", "boop", "tetta", "zinna"}
insieme_pene = {"pene", "pisello", "cazzo", "cazzetto", "mazza", "bastone", "arnese", "manganello", "cazzone",
                "gingillo", "minchia", "lalla"}
insieme_negro = {r"neg?r\w", "nigga"}
insieme_culo = {"culo", "lato ?b", "deretano",
                "fondoschiena", "natiche", "natica", "sedere"}


def command_handler(self, update: Update, context: CallbackContext):
    testo = str(update.effective_message.text).lower()

    if any([x in testo for x in insieme_culo]):
        context.bot.sendPhoto(chat_id=update.effective_chat.id,
                              photo=open("./Foto/Culo/" + random.choice(self.__lista_culo), "rb").read())
    if any([x in testo for x in insieme_fica]):
        context.bot.sendPhoto(chat_id=update.effective_chat.id,
                              photo=open("./Foto/Fica/" + random.choice(self.__lista_fica), "rb").read())
    if any([x in testo for x in insieme_pene]):  # list comprehension
        context.bot.sendPhoto(chat_id=update.effective_chat.id,
                              photo=open("./Foto/Cazzi/" + random.choice(self.__lista_cazzi), "rb").read())
    if any([x in testo for x in insieme_tette]):
        context.bot.sendPhoto(chat_id=update.effective_chat.id,
                              photo=open("./Foto/Tette/" + random.choice(self.__lista_tette), "rb").read())


def init_foto(dispatcher):
    dispatcher.add_handler(MessageHandler(
        Filters.text, command_handler, pass_user_data=True, run_async=True))
    pass
