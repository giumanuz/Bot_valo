import asyncio
import os
import time
import json
from os import mkdir, path, chmod
from typing import final
import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters


class NetworkManagerBot:
    def __init__(self):
        __root = os.getcwd()
        #self.__user = UserManager(self.__conn, __setup, __root)
        dispatcher.add_handler(CommandHandler('start', self.start, run_async=True))
        dispatcher.add_handler(CommandHandler('menu', self.__user.menu, run_async=True))

        dispatcher.add_handler(CallbackQueryHandler(self.start, pattern='start', run_async=True))

if __name__ == '__main__':
    NetworkManagerBot()
