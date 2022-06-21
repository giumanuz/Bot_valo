from datetime import date, timedelta, time

from telegram import Update
from telegram.ext import Dispatcher, ConversationHandler, CallbackQueryHandler

from bot_components.menu import Menu
from bot_components.prenotazioni_prodigit import PrenotazioneProdigit, Aula
from utils.telegram_utils import ButtonFlowMatrix

prenotazioni_attive: dict[int, PrenotazioneProdigit] = {}


def init_prenotazione_prodigit(dispatcher: Dispatcher):
    dispatcher.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(choose_edificio,
                                           pattern="prenotazione_prodigit",
                                           run_async=True)],
        states={
            0: [CallbackQueryHandler(choose_aula, pattern=r"prodigit_edificio_[A-Z0-9]{5}")],
            1: [CallbackQueryHandler(choose_day, pattern=r"prodigit_aula_.*")],
            2: [CallbackQueryHandler(choose_orario, pattern=r"prodigit_giorno_\d{4}-\d{2}-\d{2}")]
        },
        fallbacks=[]
    ))
    Menu.register_button("Prenotazione", "prenotazione_prodigit")


def choose_edificio(update: Update, _):
    markup_matrix = ButtonFlowMatrix(row_length=2)
    markup_matrix.append("RM021", callback_data="prodigit_edificio_RM021")
    markup_matrix.append("RM025", callback_data="prodigit_edificio_RM025")

    update.callback_query.edit_message_text(
        text="Scegli edificio",
        reply_markup=markup_matrix.keyboard_markup
    )
    return 0


def choose_aula(update: Update, _):
    edificio = update.callback_query.data.split('_')[-1]
    aule = [a for a in Aula if a.get_codice_edificio() == edificio]
    matrix = ButtonFlowMatrix(row_length=3)
    for aula in aule:
        matrix.append(aula.get_nome_aula(), f"prodigit_aula_{aula.value}")
    update.callback_query.edit_message_text(
        "Scegli aula", reply_markup=matrix.keyboard_markup
    )
    return 1


def get_days_matrix():
    matrix = ButtonFlowMatrix(row_length=3)
    i = 0
    while i < 9:
        giorno = date.today() + timedelta(days=i)
        if giorno.weekday() != 6:
            stringa_giorno = giorno.strftime("%d/%m")
            matrix.append(stringa_giorno, callback_data=giorno.isoformat())
            i += 1
    return matrix


TEMP_CONFIG = ("1956565", "Password", "email@gmail.com", "Sellino", "Chompy")


def choose_day(update: Update, _):
    codice_aula = update.callback_query.data.split('_')[-1]
    aula: Aula = None
    for a in Aula:
        if a.value == codice_aula:
            aula = a
            break
    prenotazioni_attive[update.effective_user.id] = PrenotazioneProdigit(*TEMP_CONFIG, aula)

    # matrix = get_days_matrix()
    # update.callback_query.edit_message_text("Scegli il giorno", reply_markup=matrix.list)
    matrix = ButtonFlowMatrix(1)
    matrix.append("Prenota la settimana", "prodigit_giorno_2022-06-21")
    update.callback_query.edit_message_reply_markup(matrix.keyboard_markup)
    return 2


def choose_orario(update: Update, _):
    user_id = update.effective_user.id
    p = prenotazioni_attive[user_id]
    giorno_iso = update.callback_query.data.split('_')[-1]
    giorno = date.fromisoformat(giorno_iso)
    p.add_day(giorno, time(9, 00), time(15, 00))
    p.prenota()
    return ConversationHandler.END
