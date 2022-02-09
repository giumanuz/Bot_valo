from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, Dispatcher
from .tris import Tris


class Menu:

    @staticmethod
    def get_command_name():
        return "menu"

    @staticmethod
    def command_handler_menu(_, update, context):
        command_list = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(
                    text=Tris.get_command_name(),
                    callback_data=Tris.get_command_pattern()
                )
            ]]
        )
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Inserisci la scelta',
                                 reply_markup=command_list)


def init_menu(dispatcher: Dispatcher) -> None:
    dispatcher.add_handler(CommandHandler(
        Menu.get_command_name(), Menu.command_handler_menu, run_async=True))
