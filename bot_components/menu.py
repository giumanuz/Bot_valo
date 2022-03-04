from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import CommandHandler, Dispatcher

from bot_components.games.tris import init_tris
from .games.snake import init_snake
from .prenotazioni import init_prenotazioni, Prenotazione


def show_menu(update: Update, _):
    command_list = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Tris",
                    callback_data="tris-callback"
                ),
                InlineKeyboardButton(
                    text="Snake",
                    callback_data="snake-callback"

                )
            ],
            [
                InlineKeyboardButton(
                    text="Prenotazione",
                    callback_data=Prenotazione.callback_id()
                )
            ]
        ]
    )
    update.effective_message.reply_text('Inserisci la scelta',
                                        reply_markup=command_list)


def init_menu(dispatcher: Dispatcher):
    dispatcher.add_handler(CommandHandler("Menu", show_menu, run_async=True))
    init_prenotazioni(dispatcher)
    init_tris(dispatcher)
    init_snake(dispatcher)
