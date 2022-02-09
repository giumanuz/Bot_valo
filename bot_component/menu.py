from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext, Dispatcher
from tris import Tris


class Menu:
    def get_command_name():
        return "menu"

    def command_handler(self, update, context):
        command_list = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=Tris.get_command_name(), callback_data=Tris.get_command_pattern())]])
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Inserisci la scelta',
                                 reply_markup=command_list)
    pass


def init_menu(dispatcher: Dispatcher) -> None:
    menu = Menu()
    dispatcher.add_handler(CommandHandler(
        menu.get_command_name(), menu.command_handler, run_async=True))
    pass
