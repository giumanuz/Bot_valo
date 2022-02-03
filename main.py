import random
from os import listdir

from compleanni import compleanni
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from threading import Thread


class Mine:

    def __init__(self):
        self.__array_list = None
        self.__corrent_player = None
        self.__lista_culo = []
        self.__lista_fica = []
        self.__lista_tette = []

        updater = Updater(token="5284256332:AAHv1djfMG6QQTobd-H_jUDpmsjvMgewpNM", use_context=True)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler('menu', self.menu, run_async=True))

        dispatcher.add_handler(CallbackQueryHandler(self.tris, pattern='tris', run_async=True))
        dispatcher.add_handler(CallbackQueryHandler(self.update_tris, pattern="\d", ))

        dispatcher.add_handler(MessageHandler(Filters.text, self.handler, pass_user_data=True, run_async=True))

        self.__lista_tette = listdir("./Foto/Tette")
        if '.DS_Store' in self.__lista_tette:
            self.__lista_tette.remove('.DS_Store')
        self.__lista_fica = listdir("./Foto/Fica")
        if '.DS_Store' in self.__lista_fica:
            self.__lista_fica.remove('.DS_Store')
        self.__lista_culo = listdir("./Foto/Culo")
        if '.DS_Store' in self.__lista_culo:
            self.__lista_culo.remove('.DS_Store')

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
            self.__array_list[riga][colonna] = InlineKeyboardButton(text="⭕", callback_data="-1")
        else:
            self.__array_list[riga][colonna] = InlineKeyboardButton(text="❌️", callback_data="-1")
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

        insulti = ["sei più inutile di un preservativo per Dag", "sei proprio un Cioppy",
                   "tua madre è una grande tartaruga",
                   "possano le tue orecchie diventare buchi di culo e defecarti sulle spalle",
                   "sei come la minchia: sempre tra le palle",
                   "sei così spaventoso che quando caghi la tua stessa merda dice di fotterti!",
                   "quando Dio diede l'intelligenza all'umanità tu dov'eri? Al cesso!?",
                   "sei cosi brutto che chi ti guarda vomita",
                   "sei cosi ignorante che pure i tuo amici ti stanno lontano",
                   "sei cosi scemo che guardi pure peppa pig",
                   "tua madre é peggio di un canestro da basket, gli entrano tutte le palle",
                   "io non capisco se sei cretino di tuo oppure ci hai studiato per esserlo",
                   "chiedi a tua mamma se sono frocio",
                   "sei così brutto che quando sei nato tua mamma ha inviato i biglietti di scuse a tutti",
                   "fai così schifo che quando ti guardi allo specchio lui si gira dall'altra parte",
                   "tua mamma ce l'ha così pelosa che per depilarsela deve chiamare la guardia forestale",
                   "tua madre è come Rowenta.. per chi non si accontenta",
                   "come ti senti se ti dico che sei solo uno schizzo di sborra di tuo padre?",
                   "di a tua madre di smettere di cambiare rossetto! Ho il pisello che sembra un arcobaleno!",
                   "lo sai perchè sulla bandiera della Mongolia c'é la tua faccia? Perché sei il re dei mongoloidi",
                   "tua mamma è come gli orsi: sempre in cerca di pesce",
                   "sei cosi brutto ma cosi brutto che tua mamma appena ti ha fatto pensava che fossi uscito dal culo",
                   "tua madre ha visto più tubi di tutta la saga di Super Mario",
                   "tua mamma si mette le prugne in culo e ci fa la marmellata", "ti puzza la minchia",
                   "sei cosi testa di cazzo che quando un'uomo pensa a te puo diventare gay!",
                   "le tue gambe sono così pelose che per farti la ceretta devi affittare un tagliaerba",
                   "io ti penso spesso.. ma quando sono al cesso!",
                   "tua madre è come Buffon, ha sempre palle tra le mani",
                   "che cos'è una disgrazia? Conoscerti e incontrarti",
                   "ma tu sei nato male o tuo padre ha usato il preservativo bucato?",
                   "non ti prendo a calci perché potrebbe piacerti",
                   "tua mamma e come i mobili dell'ikea: tutti se la montano",
                   "tua mamma e come un gelato: se la gustano tutti",
                   "sei così brutto che quando accendi il computer si attiva subito l'antivirus",
                   "sei così brutto che se i testimoni di geova vengono a casa tua, si chiudono la porta in faccia da soli",
                   "non ti sputo addosso, perché la mia saliva ti disinfetterebbe",
                   "sei così brutto che quando vai al mare viene la bassa marea"]
        insieme_fica = {"vagina", "fica", "pisella", "fregna", "figa", "utero", "vulva", "gnegna"}
        insieme_tette = {"tette", "zinne", "seno", "coseno", "poppe", "mammelle", "boops", "boop", "tetta", "zinna"}
        insieme_pene = {"pene", "pisello", "cazzo", "cazzetto", "mazza", "bastone", "arnese", "manganello", "cazzone",
                        "gingillo", "minchia"}
        insieme_negro = {"neg?r\w", "nigga"}
        insieme_culo = {"culo", "lato ?b", "deretano", "fondoschiena", "natiche", "natica", "sedere"}
        lista_cazzi = ["./Foto/2.jpeg", "./Foto/3.jpeg", "./Foto/4.jpeg"]
        lista_fiche = ["./Foto/5.jpeg", "./Foto/6.jpeg", "./Foto/6.jpeg", "./Foto/7.jpeg", "./Foto/8.jpeg",
                       "./Foto/9.jpeg", "./Foto/10.jpeg", "./Foto/11.jpeg", "./Foto/12.jpeg", "./Foto/13.jpeg",
                       "./Foto/14.jpeg", "./Foto/15.jpeg", "./Foto/16.jpeg", "./Foto/17.jpeg"]

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

        if any([x in testo for x in insieme_culo]):
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=open("./Foto/Culo/" + random.choice(self.__lista_culo), "rb").read())
        if any([x in testo for x in insieme_fica]):
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=open("./Foto/Fica/" + random.choice(self.__lista_fica), "rb").read())
        if any([x in testo for x in insieme_pene]):  # list comprehension
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=open(random.choice(lista_cazzi), "rb").read())
        if any([x in testo for x in insieme_tette]):
            context.bot.sendPhoto(chat_id=update.effective_chat.id,
                                  photo=open("./Foto/Tette/" + random.choice(self.__lista_tette), "rb").read())
        if "botvalo" in testo:
            if "insulta" in testo:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=f'Cioppy {random.choice(insulti)}')  # format string
            if "è 30l" in testo:
                context.bot.send_message(chat_id=update.effective_chat.id, text='Per penitenza devi scrivere a Lalla')

            if "dettu de derni" in testo:
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text='Quannu Cesi ha lu cappello, turna \'ndietro e pija l\'umbrello')


if __name__ == '__main__':
    Mine()
