import random
from compleanni import compleanni
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from threading import Thread


class Mine:

    def __init__(self):
        self.__array_list = None
        self.__corrent_player = None

        updater = Updater(token="5284256332:AAHv1djfMG6QQTobd-H_jUDpmsjvMgewpNM", use_context=True)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler('menu', self.menu, run_async=True))

        dispatcher.add_handler(CallbackQueryHandler(self.tris, pattern='tris', run_async=True))
        dispatcher.add_handler(CallbackQueryHandler(self.update_tris, pattern="\d", ))

        dispatcher.add_handler(MessageHandler(Filters.text, self.handler, pass_user_data=True, run_async=True))

        # t = Thread(target= compleanni, args=[updater.])
        #  t.start()
        updater.start_polling()
        updater.idle()

    def menu(self, update, context):
        name = update.message.chat.first_name
        chat_id = update.effective_chat.id

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Inserisci la scelta',
                                 reply_markup=InlineKeyboardMarkup(
                                     [[InlineKeyboardButton(text="Tris",
                                                            callback_data="tris")]]))

    def tris(self, update, context):
        self.__array_list = [[InlineKeyboardButton(text="🟢️", callback_data="0"),
                              InlineKeyboardButton(text="🟢", callback_data="1"),
                              InlineKeyboardButton(text="🟢", callback_data="2")],
                             [InlineKeyboardButton(text="🟢", callback_data="3"),
                              InlineKeyboardButton(text="🟢", callback_data="4"),
                              InlineKeyboardButton(text="🟢", callback_data="5")],
                             [InlineKeyboardButton(text="🟢", callback_data="6"),
                              InlineKeyboardButton(text="🟢", callback_data="7"),
                              InlineKeyboardButton(text="🟢", callback_data="8")]]

        self.__corrent_player = 0

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Ecco il tris",
                                 reply_markup=InlineKeyboardMarkup(self.__array_list))

    def update_tris(self, update: Update, context: CallbackContext):
        update.callback_query.answer()
        numero = int(update.callback_query.data)
        if numero == -1:
            return
        riga = numero // 3
        colonna = numero % 3
        if self.__corrent_player:
            self.__array_list[riga][colonna] = InlineKeyboardButton(text="❌", callback_data="-1")
        else:
            self.__array_list[riga][colonna] = InlineKeyboardButton(text="⭕️", callback_data="-1")
        self.__corrent_player = not self.__corrent_player
        update.callback_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(self.__array_list))

    def handler(self, update, context):
        testo = str(update.effective_message.text).lower()
        print(testo)
        message_id = update.effective_message.message_id
        # invio di un messaggio
        # context.bot.send_message(chat_id=update.effective_chat.id,
        #                                   text="Signore il suo account è già stato attivato correttemente, si rechi al menu per i possibili comandi.",
        #                                      reply_markup=InlineKeyboardMarkup(
        #                                          [[InlineKeyboardButton(text="Menu", callback_data="menu")]]))
        # modifica di un messaggio
        # context.bot.editMessageText(chat_id=update.effective_chat.id,
        #                                    message_id=step[1],
        #                                    text="Comando non riconosciuto, riprova❗")

        insulti = ["sei più inutile di un preservativo per Dag", "sei proprio un Cioppy"]
        insieme_fica = {"vagina", "fica", "pisella", "fregna", "figa", "utero", "vulva", "gnegna"}
        insieme_tette = {"tette", "zinne", "seno", "coseno", "poppe", "mammelle", "boops", "boop", "tetta", "zinna"}
        insieme_pene = {"pene", "pisello", "cazzo", "cazzetto", "mazza", "bastone", "arnese", "manganello", "cazzone",
                        "gingillo"}
        insieme_negro = {"neg?r\w", "nigga"}
        insieme_culo = {"culo", "lato ?b", "deretano", "fondoschiena", "natiche", "natica", "sedere"}
        lista_cazzi = ["./Foto/2.jpeg", "./Foto/3.jpeg", "./Foto/4.jpeg"]

        if "grazie" in testo:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Ar cazzo')

        if "apple" in testo:
            context.bot.send_message(chat_id=update.effective_chat.id, text='Apple >>>> Winzoz')

        if "windows" in testo:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text='Ma chi cazzo usa ancora quella merda di Winzoz')

        if "paolo" in testo:
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo="http://www.diag.uniroma1.it/~digiamb/website/Files/foto.jpg",
                                  caption="MMM che manzo")

        if "culo" in testo:
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo="https://pbs.twimg.com/profile_images/538777115127455744/NRffC4u8_400x400.jpeg")
        if "fica" in testo:
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo="https://www.lapecorasclera.it/public/immagini_pecora/NATURALE-5.jpg")
        if any([x in testo for x in insieme_cazzi]):  # list comprehension
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=open(random.choice(lista_cazzi), "rb").read())

        if "tette" in testo:
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=open("./Foto/1.jpg", "rb").read())
        if "botvalo" in testo:
            if "insulta" in testo:
                lista = testo.split(" ")
                posizione = lista.index("insulta")
                nome = lista[posizione + 1]
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=f'{nome} {random.choice(insulti)}')  # format string
            if "è 30l" in testo:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Eliminare Cioppy')
            if "dettu de derni" in testo:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text='Quannu Cesi ha lu cappello, turna \'ndietro e pija l\'umbrello')


if __name__ == '__main__':
    Mine()
