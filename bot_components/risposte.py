import random

from telegram import Update
from telegram.ext import CallbackContext


class Risposte:

    @staticmethod
    def linguaggi(chat_id: int, testo: str, context: CallbackContext):
        if "py" in testo:
            context.bot.send_message(
                chat_id=chat_id, text='Python merdaaaaaaaaaa')

        if "java" in testo:
            context.bot.send_message(
                chat_id=chat_id, text='mannaggia ai funtori')

        if "c#" in testo:
            context.bot.send_message(
                chat_id=chat_id, text='COOL C-Like Object Oriented Language')
            
        if "c++" in testo:
            context.bot.send_message(chat_id=chat_id,
                                     text=random.choice(('Lu meju', 'TipoNodoSCL ma con le classi')))

    @staticmethod
    def software(chat_id: int, testo: str, context: CallbackContext):
        if "apple" in testo:
            context.bot.send_message(
                chat_id=chat_id, text='Apple >>>> Winzoz')

        if "windows" in testo:
            context.bot.send_message(chat_id=chat_id,
                                     text='Ma chi cazzo usa ancora quella merda di Winzoz')

        if "linux" in testo:
            context.bot.send_message(chat_id=chat_id,
                                     text='Che hacker che sei!')

        if "intellij" in testo:
            context.bot.send_message(chat_id=chat_id,
                                     text='i pro usano nano')

    @staticmethod
    def universita(chat_id: int, testo: str, context: CallbackContext):
        if "paolo" in testo:
            context.bot.sendPhoto(chat_id=chat_id,
                                  photo="https://www.diag.uniroma1.it/~digiamb/website/Files/foto.jpg",
                                  caption="MMM che manzo")

        if "è 30l" in testo:
            context.bot.send_message(
                chat_id=chat_id, text='Per penitenza devi scrivere a Lalla')

        if "banal" in testo:
            context.bot.send_message(
                chat_id=chat_id, text='tanto è 30L')

        if "ricorsione" in testo:
            context.bot.send_message(
                chat_id=chat_id, text='La ricorsione è per naBBoltenati')

        if "oro" in testo:
            context.bot.send_message(
                chat_id=chat_id, text='Oro Colato!')

    @staticmethod
    def generici(chat_id: int, testo: str, context: CallbackContext):
        if "grazie" in testo:
            context.bot.send_message(chat_id=chat_id, text='Ar cazzo')

        if "cosa?" in testo:
            context.bot.send_message(chat_id=chat_id, text='Stocazzoooo!')

        if "ə" in testo:
            context.bot.send_message(chat_id=chat_id, text='Ricchionǝ')

        if "ma è un uomo" in testo:
            context.bot.send_message(
                chat_id=chat_id, text='E allora sei gay')

    @staticmethod
    def handle_message(update: Update, context: CallbackContext):
        testo = str(update.effective_message.text).lower()
        chat_id: int = update.effective_chat.id

        Risposte.linguaggi(chat_id, testo, context)
        Risposte.software(chat_id, testo, context)
        Risposte.universita(chat_id, testo, context)
        Risposte.generici(chat_id, testo, context)

        if "botvalo" in testo:
            if "dettu de derni" in testo:
                context.bot.send_message(chat_id=chat_id,
                                         text='Quannu Cesi ha lu cappello, turna \'ndietro e pija l\'umbrello')

        # test
        if chat_id == -1 and "test" in testo:
            context.bot.send_message(chat_id=-1,
                                     text='test')
