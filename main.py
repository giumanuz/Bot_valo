from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters


class Mine:

    def __init__(self):
        updater = Updater(token="5284256332:AAHv1djfMG6QQTobd-H_jUDpmsjvMgewpNM", use_context=True)
        dispatcher = updater.dispatcher
        #dispatcher.add_handler(CommandHandler('start', self.start, run_async=True))

        #dispatcher.add_handler(CallbackQueryHandler(self.hello, pattern='hello', run_async=True))

        dispatcher.add_handler(MessageHandler(Filters.text, self.handler, pass_user_data=True, run_async=True))

        updater.start_polling()
        updater.idle()

    def start(self, update, context):
        name = update.message.chat.first_name
        chat_id = update.effective_chat.id

        #context.bot.send_message(chat_id=update.effective_chat.id,
         #                        text='Ciao bello',
          #                       reply_markup=InlineKeyboardMarkup(
           #                          [[InlineKeyboardButton(text="Ardimme ciao",
            #                                                callback_data="hello")]]))

    def hello(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Allora si scemo, tho appena salutato!',
                                 reply_markup=InlineKeyboardMarkup(
                                     [[InlineKeyboardButton(text="Ardimme ciao",
                                                            callback_data="hello")]]))

    def handler(self, update, context):
        testo = str(update.effective_message.text).lower()
        print (testo)
        message_id = update.effective_message.message_id
        # invio di un messaggio
        # context.bot.send_message(chat_id=update.effective_chat.id,
        #                                      text="Signore il suo account è già stato attivato correttemente, si rechi al menu per i possibili comandi.",
        #                                      reply_markup=InlineKeyboardMarkup(
        #                                          [[InlineKeyboardButton(text="Menu", callback_data="menu")]]))
        # modifica di un messaggio
        # context.bot.editMessageText(chat_id=update.effective_chat.id,
        #                                    message_id=step[1],
        #                                    text="Comando non riconosciuto, riprova❗")
        if "grazie" in testo:
            context.bot.send_message(chat_id=update.effective_chat.id, text='<Ar cazzo>')

        elif "apple" in testo:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Apple >>>> Winzoz')

        elif "windows" in testo:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Ma chi cazzo usa ancora quella merda di Winzoz')

        elif "paolo" in testo:
            context.bot.sendPhoto(chat_id=update.effective_chat.id, photo="http://www.diag.uniroma1.it/~digiamb/website/Files/foto.jpg", caption="MMM che manzo")

        elif "culo" in testo:
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo="https://pbs.twimg.com/profile_images/538777115127455744/NRffC4u8_400x400.jpeg")
        elif "fica" in testo:
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo="data:image/jpeg;base64,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")

        elif ("cazzo" or "pene") in testo:
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo="https://i1.sndcdn.com/artworks-000452488116-6ef7g4-t500x500.jpg")

        elif "tette" in testo:
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo="data:image/jpeg;base64,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")

        elif "botvalo" in testo:
            if "insulta cioppy" in testo:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Cioppy è gay')
            elif "è 30l" in testo:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Eliminare Cioppy')
            elif "dettu de derni" in testo:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Quannu Cesi ha lu cappello, turna \'ndietro e pija l\'umbrello')




if __name__ == '__main__':
    Mine()
