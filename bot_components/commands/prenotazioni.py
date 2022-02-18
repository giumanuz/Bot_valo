from __future__ import annotations

import json
import os
import random

import qrcode
from fpdf import FPDF
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, Filters, MessageHandler, \
    CallbackQueryHandler, Dispatcher


def fetch_files():
    dichiarazione_path = os.path.join(os.path.dirname(__file__), "dichiarazione.json")
    settings_path = os.path.join(os.path.dirname(__file__), "frasi.json")

    with open(dichiarazione_path, 'r', encoding='UTF-8') as f:
        testo_dichiarazione = json.load(f)

    with open(settings_path, 'r', encoding='UTF-8') as f:
        settings = json.load(f)

    return testo_dichiarazione, settings


class Prenotazione:
    testo_dichiarazione, settings = fetch_files()

    color = settings["color"]
    size = settings["size"]
    texts = settings["texts"]

    prenotazioni_in_corso = {}

    def __init__(self, id_persona):
        self.id_persona = id_persona
        self.matricola = None
        self.nome = None
        self.giorno = None
        self.aula = None
        self.edificio = None
        self.dalle = None
        self.alle = None

    def __str__(self):
        return f"{self.matricola} {self.nome} {self.giorno} {self.aula} {self.edificio} {self.dalle} {self.alle}"

    @staticmethod
    def get_command_name():
        return "Prenotazione"

    @staticmethod
    def get_command_pattern():
        return r"\d"

    @classmethod
    def chooseEdificio(cls, update: Update, _):
        chat_id = update.effective_chat.id
        id_persona = update.callback_query.from_user.id
        cls.prenotazioni_in_corso[chat_id] = Prenotazione(id_persona)

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

    @classmethod
    def chooseAula(cls, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        num_edificio = update.callback_query.data
        cls.prenotazioni_in_corso[chat_id].edificio = num_edificio
        context.bot.send_message(chat_id=update.effective_chat.id, text="Inserisci l'Aula")
        return 1

    @classmethod
    def chooseGiorno(cls, update, context):
        chat_id = update.effective_chat.id
        aula = update.message.text
        cls.prenotazioni_in_corso[chat_id].aula = aula
        context.bot.send_message(chat_id=update.effective_chat.id, text="Inserisci il giorno (dd/mm/aaaa)")
        return 2

    @classmethod
    def chooseDalle(cls, update, context):
        chat_id = update.effective_chat.id
        num_giorno = update.message.text
        cls.prenotazioni_in_corso[chat_id].giorno = num_giorno
        context.bot.send_message(chat_id=update.effective_chat.id, text="Inserisci da che ora vuoi prenotare (hh)")
        return 3

    @classmethod
    def chooseAlle(cls, update, context):
        chat_id = update.effective_chat.id
        num_dalle = update.message.text
        cls.prenotazioni_in_corso[chat_id].dalle = num_dalle
        context.bot.send_message(chat_id=update.effective_chat.id, text="Inserisci fino a che ora vuoi prenotare (hh)")
        return 4

    @classmethod
    def choosePersona(cls, update, context):
        chat_id = update.effective_chat.id
        num_alle = update.message.text
        cls.prenotazioni_in_corso[chat_id].alle = num_alle
        context.bot.send_message(chat_id=update.effective_chat.id, text="Inserisci la persona (Nome Cognome)")
        return 5

    @classmethod
    def chooseMatricola(cls, update, context):
        chat_id = update.effective_chat.id
        nome = update.message.text
        cls.prenotazioni_in_corso[chat_id].nome = nome
        context.bot.send_message(chat_id=update.effective_chat.id, text="Inserisci la matricola")
        return 6

    @classmethod
    def ultima_funzione(cls, update, context):
        chat_id = update.effective_chat.id
        matricola = update.message.text
        cls.prenotazioni_in_corso[chat_id].matricola = matricola
        num = cls.pdf_main(prenotazione=cls.prenotazioni_in_corso[chat_id])
        cls.prenotazioni_in_corso.pop(chat_id)

        context.bot.sendDocument(chat_id=chat_id, document=open(num + ".pdf", 'rb'))
        os.remove(num + ".pdf")
        return ConversationHandler.END

    @classmethod
    def fine(cls, update, context):
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=update.effective_chat.id, text="Annullata la prenotazione")
        cls.prenotazioni_in_corso.pop(chat_id)
        return ConversationHandler.END

    @classmethod
    def pdf_main(cls, prenotazione: Prenotazione) -> str:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B")

        num = cls.crea_qr(prenotazione)

        pdf.image(f'{num}.png', x=80, y=10, w=60, h=60)
        os.remove(f'{num}.png')
        pdf.cell(0, 70, ln=1)

        for riga in Prenotazione.texts:
            cls.aggiungi_riga(pdf, riga, prenotazione)

        pdf.output(f'{num}.pdf')
        return num

    @classmethod
    def crea_qr(cls, prenotazione) -> str:
        matricola = prenotazione.matricola
        edificio = prenotazione.edificio
        giorno = prenotazione.giorno
        qr = qrcode.make(f"{matricola},{giorno},RM02{edificio}")
        type(qr)
        num = str(random.randint(1, 10000))
        qr.save(f'{num}.png')
        return num

    @classmethod
    def aggiungi_riga(cls, pdf: FPDF, riga, prenotazione: Prenotazione):
        matricola = prenotazione.matricola
        edificio = prenotazione.edificio
        aula = prenotazione.aula
        nome = prenotazione.nome
        dalle = prenotazione.dalle
        alle = prenotazione.alle
        giorno = prenotazione.giorno
        if edificio == "1":
            via = 'Circonvallazione Tibuertina, 4'
            collocazione = "Edificio Marco Polo (ex Poste S. Lorenzo)"
        elif edificio == "5":
            via = 'Via Tiburtina, 205'
            collocazione = "- Aule (Via Tiburtina))"
        else:
            raise Exception("Cannot get here")

        for i in range(len(riga)):
            blocchetto = riga[i]
            pdf.set_font("Arial", "B", size=cls.size[blocchetto["size"]])

            colore = cls.color[blocchetto["color"]]
            pdf.set_text_color(colore[0], colore[1], colore[2])

            testo = blocchetto["text"]

            if testo == "{dichiarazione}":
                for pezzo in cls.testo_dichiarazione:
                    pdf.multi_cell(0, 6, pezzo, 0)
                    pdf.cell(0, 4, "", ln=1)
                continue

            testo = str.format(testo,
                               nome=nome,
                               matricola=matricola,
                               giorno=giorno,
                               aula=aula,
                               edificio=edificio,
                               via=via,
                               collocazione=collocazione,
                               inizio=dalle,
                               fine=alle)

            ln = 0
            if i == len(riga) - 1:
                ln = 1

            pdf.cell(pdf.get_string_width(testo), 8, testo, ln=ln)


def init_prenotazioni(dispatcher: Dispatcher):
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
            ],
            6: [
                MessageHandler(Filters.text & ~Filters.command, Prenotazione.ultima_funzione)
            ]
        },
        fallbacks=[CommandHandler("quit", Prenotazione.fine)]

    ))
