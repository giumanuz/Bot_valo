import random

from telegram import Update
from telegram.ext import CallbackContext

from bot_components.utils.regex_parser import contains


class Risposte:

    @staticmethod
    def linguaggi(chat_id: int, testo: str, context: CallbackContext):
        if contains("py", testo):
            context.bot.send_message(
                chat_id=chat_id, text='Python merdaaaaaaaaaa')

        if contains("java", testo):
            context.bot.send_message(
                chat_id=chat_id, text='mannaggia ai funtori')

        if contains(r"c\#", testo):
            context.bot.send_message(
                chat_id=chat_id, text='COOL C-Like Object Oriented Language')

        if contains(r"c\+\+", testo):
            context.bot.send_message(chat_id=chat_id,
                                     text=random.choice(('Lu meju', 'TipoNodoSCL ma con le classi')))

    @staticmethod
    def software(chat_id: int, testo: str, context: CallbackContext):
        if contains("apple", testo):
            context.bot.send_message(
                chat_id=chat_id, text='Apple >>>> Winzoz')

        if contains("windows", testo):
            context.bot.send_message(chat_id=chat_id,
                                     text='Ma chi cazzo usa ancora quella merda di Winzoz')

        if contains("linux", testo):
            context.bot.send_message(chat_id=chat_id,
                                     text='Che hacker che sei!')

        if contains("intellij", testo):
            context.bot.send_message(chat_id=chat_id,
                                     text='i pro usano nano')

    @staticmethod
    def universita(chat_id: int, testo: str, context: CallbackContext):
        if contains("paolo", testo):
            context.bot.sendPhoto(chat_id=chat_id,
                                  photo="https://www.diag.uniroma1.it/~digiamb/website/Files/foto.jpg",
                                  caption="MMM che manzo")

        if contains("è 30l", testo):
            context.bot.send_message(
                chat_id=chat_id, text='Per penitenza devi scrivere a Lalla')

        if contains("banal", testo):
            context.bot.send_message(
                chat_id=chat_id, text='tanto è 30L')

        if contains("ricorsione" in testo or "ricorsiv", testo):
            context.bot.send_message(
                chat_id=chat_id, text='La ricorsione è per naBBoltenati')

        if contains("oro", testo):
            context.bot.send_message(
                chat_id=chat_id, text='Oro Colato!')

    @staticmethod
    def generici(chat_id: int, testo: str, context: CallbackContext):
        if contains("grazie", testo):
            context.bot.send_message(chat_id=chat_id, text='Ar cazzo')

        if contains(r"cosa\?", testo) or contains(r"che\?", testo):
            context.bot.send_message(chat_id=chat_id, text='Stocazzoooo!')

        if contains("ə", testo):
            context.bot.send_message(chat_id=chat_id, text='Ricchionə')

        if contains("ma è un uomo", testo):
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

        if contains("botvalo", testo):
            if contains("dettu de derni", testo):
                context.bot.send_message(chat_id=chat_id,
                                         text="Quannu Cesi ha lu cappello, turna 'ndietro e pija l'umbrello")
