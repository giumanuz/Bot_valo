from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, Dispatcher, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

from .tris import Tris


class Prenotazione:
    @staticmethod
    def get_command_name():
        return "Prenotazione"

    @staticmethod
    def get_command_pattern():
        return "\d"

    @staticmethod
    def chooseEdificio(update, context):
        update.callback_query.answer()
        command_list = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(
                    text="RM021",
                    callback_data="1"
                ),
                InlineKeyboardButton(
                    text="RM025",
                    callback_data="5"
                )
            ]
            ]
        )
        update.callback_query.edit_message_text(text="Scegli Edificio")
        update.callback_query.edit_message_reply_markup(
            reply_markup=command_list)

        return 0

    @staticmethod
    def chooseAula(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Inserisci l'Aula")
        return 1

    @staticmethod
    def chooseGiorno(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Inserisci il giorno (dd/mm/aaaa)")
        return 2

    @staticmethod
    def chooseDalle(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Inserisci da che ora vuoi prenotare (hh)")
        return 3

    @staticmethod
    def chooseAlle(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Inserisci fino a che ora vuoi prenotare (hh)")
        return 4

    @staticmethod
    def choosePersona(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Inserisci la persona (NOME COGNOME)")
        return 5

    @staticmethod
    def chooseMatricola(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Inserisci la matricola")
        return ConversationHandler.END

    @staticmethod
    def fine(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Annullata la prenotazione")
        return ConversationHandler.END

class Menu:
    @staticmethod
    def get_command_name():
        return "menu"

    @staticmethod
    def handle_command(update, context):
        command_list = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(
                    text=Tris.get_command_name(),
                    callback_data=Tris.get_command_pattern()
                ),
                InlineKeyboardButton(
                    text=Prenotazione.get_command_name(),
                    callback_data=Prenotazione.get_command_name()
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

    dispatcher.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(Prenotazione.chooseEdificio, pattern=Prenotazione.get_command_name(),
                                          run_async=True)],
        states={
            0: [
                CallbackQueryHandler(Prenotazione.chooseAula, pattern=r"\d")
            ],
            1: [
                MessageHandler(Filters.text & ~Filters.command, Prenotazione.chooseGiorno)
            ],
            2: [
                MessageHandler(Filters.text & ~Filters.command, Prenotazione.chooseDalle)
            ],
            3: [
                MessageHandler(Filters.text & ~Filters.command, Prenotazione.chooseAlle)
            ],
            4: [
                MessageHandler(Filters.text & ~Filters.command, Prenotazione.choosePersona)
            ],
            5: [
                MessageHandler(Filters.text & ~Filters.command, Prenotazione.chooseMatricola)
            ]
        },
        fallbacks=[CommandHandler("quit", Prenotazione.fine)]

    ))
