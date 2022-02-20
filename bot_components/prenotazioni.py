import json
import os
from random import randint

import qrcode
from fpdf import FPDF
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, Filters, MessageHandler, \
    CallbackQueryHandler, Dispatcher

from .utils.os_utils import get_absolute_path


def remove_file_from_top_directory(filename: str):
    os.remove(get_absolute_path(f"/{filename}"))


def load_prenotation_files():
    dichiarazione_path = get_absolute_path("/resources/prenotazioni/dichiarazione.json")
    settings_path = get_absolute_path("/resources/prenotazioni/settings_prenotazioni.json")
    with open(dichiarazione_path, 'r', encoding='UTF-8') as f:
        testo_dichiarazione = json.load(f)
    with open(settings_path, 'r', encoding='UTF-8') as f:
        settings = json.load(f)
    return testo_dichiarazione, settings


class Prenotazione:
    testo_dichiarazione, settings = load_prenotation_files()

    text_colors = settings["color"]
    text_sizes = settings["size"]
    texts = settings["texts"]

    prenotazioni_in_corso = {}

    @staticmethod
    def callback_id():
        return "prenotazione"

    def __init__(self):
        self.matricola = None
        self.nome = None
        self.giorno = None
        self.aula = None
        self.edificio = None
        self.dalle = None
        self.alle = None
        self.pdf = FPDF()
        self.id = randint(0, 10000)

    def generate_pdf(self):
        self.initialize_pdf()
        self.insert_qr()
        for riga in self.texts:
            self.aggiungi_riga(riga)
        self.pdf.output(f"{self.id}.pdf")

    def initialize_pdf(self):
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B")

    def insert_qr(self):
        qr_image_file = self.generate_qr()
        self.pdf.image(qr_image_file, x=80, y=10, w=60, h=60)
        remove_file_from_top_directory(qr_image_file)
        self.pdf.cell(0, 65, ln=1)

    def generate_qr(self) -> str:
        qr = qrcode.make(f"{self.matricola},{self.giorno},RM02{self.edificio}")
        qr_image_file = f"qr-{self.id}.png"
        qr.save(qr_image_file)
        return qr_image_file

    def aggiungi_riga(self, riga):
        for elemento in riga:
            self.set_pdf_style(size=self.text_sizes[elemento["size"]],
                               color=self.text_colors[elemento["color"]])
            testo = elemento["text"]
            if testo == "{dichiarazione}":
                self.insert_dichiarazione()
                continue
            self.write_text_to_pdf(testo)
        self.pdf.ln()

    def set_pdf_style(self, size, color: tuple[int, int, int]):
        self.pdf.set_font_size(size)
        self.pdf.set_text_color(color[0], color[1], color[2])

    def insert_dichiarazione(self):
        for pezzo in self.testo_dichiarazione:
            self.pdf.multi_cell(0, 6, pezzo, 0)
            self.pdf.cell(0, 4, "", ln=1)

    def write_text_to_pdf(self, testo):
        testo = self.format_text(testo)
        self.pdf.cell(self.pdf.get_string_width(testo), 6, testo)
        if "\n" in testo:
            self.pdf.ln()

    def format_text(self, testo):
        via, collocazione = self.get_collocazione()
        return str.format(testo,
                          nome=self.nome, matricola=self.matricola,
                          giorno=self.giorno,
                          aula=self.aula, edificio=self.edificio,
                          via=via, collocazione=collocazione,
                          inizio=self.dalle, fine=self.alle)

    def get_collocazione(self):
        if self.edificio == "1":
            return "Circonvallazione Tiburtina, 4", "Edificio Marco Polo (ex Poste S. Lorenzo)"
        elif self.edificio == "5":
            return "Via Tiburtina, 205", "- Aule (Via Tiburtina)"
        else:
            raise Exception("Cannot get here")

    @classmethod
    def choose_edificio(cls, update: Update, _):
        chat_id = update.effective_chat.id
        cls.prenotazioni_in_corso[chat_id] = Prenotazione()

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
            ]]
        )
        update.callback_query.edit_message_text(text="Scegli Edificio")
        update.callback_query.edit_message_reply_markup(
            reply_markup=command_list)
        return 0

    @classmethod
    def choose_aula(cls, update: Update, context: CallbackContext):
        chat_id = update.effective_chat.id
        num_edificio = update.callback_query.data
        cls.prenotazioni_in_corso[chat_id].edificio = num_edificio
        context.bot.send_message(chat_id=chat_id, text="Inserisci l'Aula")
        return 1

    @classmethod
    def choose_giorno(cls, update, context):
        chat_id = update.effective_chat.id
        aula = update.message.text
        cls.prenotazioni_in_corso[chat_id].aula = aula
        context.bot.send_message(chat_id=chat_id, text="Inserisci il giorno (dd/mm/aaaa)")
        return 2

    @classmethod
    def choose_dalle(cls, update, context):
        chat_id = update.effective_chat.id
        num_giorno = update.message.text
        cls.prenotazioni_in_corso[chat_id].giorno = num_giorno
        context.bot.send_message(chat_id=chat_id, text="Inserisci da che ora vuoi prenotare (hh)")
        return 3

    @classmethod
    def choose_alle(cls, update, context):
        chat_id = update.effective_chat.id
        num_dalle = update.message.text
        cls.prenotazioni_in_corso[chat_id].dalle = num_dalle
        context.bot.send_message(chat_id=chat_id, text="Inserisci fino a che ora vuoi prenotare (hh)")
        return 4

    @classmethod
    def choose_persona(cls, update, context):
        chat_id = update.effective_chat.id
        num_alle = update.message.text
        cls.prenotazioni_in_corso[chat_id].alle = num_alle
        context.bot.send_message(chat_id=chat_id, text="Inserisci la persona (Nome Cognome)")
        return 5

    @classmethod
    def choose_matricola(cls, update, context):
        chat_id = update.effective_chat.id
        nome = update.message.text
        cls.prenotazioni_in_corso[chat_id].nome = nome
        context.bot.send_message(chat_id=chat_id, text="Inserisci la matricola")
        return 6

    @classmethod
    def send_pdf(cls, update, context):
        chat_id = update.effective_chat.id
        matricola = update.message.text
        prenotazione = cls.prenotazioni_in_corso[chat_id]
        prenotazione.matricola = matricola
        prenotazione.generate_pdf()
        cls.prenotazioni_in_corso.pop(chat_id)

        pdf_file_name = f"{prenotazione.id}.pdf"
        with open(pdf_file_name, 'rb') as pdf_file:
            context.bot.sendDocument(chat_id=chat_id, document=pdf_file)
        remove_file_from_top_directory(pdf_file_name)

        return ConversationHandler.END

    @classmethod
    def annulla_prenotazione(cls, update, context):
        chat_id = update.effective_chat.id
        context.bot.send_message(chat_id=chat_id, text="Prenotazione annullata")
        cls.prenotazioni_in_corso.pop(chat_id)
        return ConversationHandler.END


def init_prenotazioni(dispatcher: Dispatcher):
    dispatcher.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(Prenotazione.choose_edificio,
                                           pattern="^prenotazione$",
                                           run_async=True)],
        states={
            0: [CallbackQueryHandler(Prenotazione.choose_aula, pattern=r"\d")],
            1: [MessageHandler(Filters.text & ~Filters.command, Prenotazione.choose_giorno)],
            2: [MessageHandler(Filters.text & ~Filters.command, Prenotazione.choose_dalle)],
            3: [MessageHandler(Filters.text & ~Filters.command, Prenotazione.choose_alle)],
            4: [MessageHandler(Filters.text & ~Filters.command, Prenotazione.choose_persona)],
            5: [MessageHandler(Filters.text & ~Filters.command, Prenotazione.choose_matricola)],
            6: [MessageHandler(Filters.text & ~Filters.command, Prenotazione.send_pdf)]
        },
        fallbacks=[CommandHandler("quit", Prenotazione.annulla_prenotazione)]

    ))
