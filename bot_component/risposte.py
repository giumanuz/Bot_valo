from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext, Dispatcher


def command_handler(self, update: Update, context: CallbackContext) -> None:
    testo = str(update.effective_message.text).lower()

    if "grazie" in testo:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text='Ar cazzo')

    if "ə" in testo:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text='Ricchionǝ')

    if "apple" in testo:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text='Apple >>>> Winzoz')

    if "windows" in testo:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Ma chi cazzo usa ancora quella merda di Winzoz')

    if "paolo" in testo:
        context.bot.sendPhoto(chat_id=update.effective_chat.id,
                              photo="http://www.diag.uniroma1.it/~digiamb/website/Files/foto.jpg",
                              caption="MMM che manzo")

    if "botvalo" in testo:
        if "è 30l" in testo:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text='Per penitenza devi scrivere a Lalla')

        if "dettu de derni" in testo:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='Quannu Cesi ha lu cappello, turna \'ndietro e pija l\'umbrello')

    pass


def init_risposte(dispatcher):
    dispatcher.add_handler(MessageHandler(
        Filters.text, command_handler, pass_user_data=True, run_async=True))
    pass
