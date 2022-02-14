from telegram.ext import CommandHandler

from .games.snake import *
from .tris import *


class Menu:
    @staticmethod
    def get_command_name():
        return "menu"

    @staticmethod
    def handle_command(update, context):
        command_list = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text=Tris.get_command_name(),
                        callback_data=Tris.get_command_pattern()
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Snake",
                        callback_data="snake-callback"
                    )
                ]
            ]
        )
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Inserisci la scelta',
                                 reply_markup=command_list)


def init_menu(dispatcher: Dispatcher):
    dispatcher.add_handler(CommandHandler(
        Menu.get_command_name(), Menu.handle_command, run_async=True))
    init_tris(dispatcher)
    init_snake(dispatcher)
