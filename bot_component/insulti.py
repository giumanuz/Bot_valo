import random
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext, Dispatcher

lista_insulti = [
    "sei più inutile di un preservativo per Dag",
    "sei proprio un Cioppy",
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
    "sei così brutto che quando vai al mare viene la bassa marea"
]


def command_handler(self, update: Update, context: CallbackContext) -> None:
    testo = str(update.effective_message.text).lower()

    if "insulta" in testo:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'Cioppy {random.choice(lista_insulti)}')  # format string
    pass


def init_insulti(dispatcher):
    dispatcher.add_handler(MessageHandler(
        Filters.text, command_handler, pass_user_data=True, run_async=True))
    pass
