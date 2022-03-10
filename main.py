import logging
from os import environ as environment_variables

import firebase_admin
from dotenv import load_dotenv
from firebase_admin.credentials import Certificate
from telegram.ext import Updater

from bot_components.firebase_manager import FirebaseApp
from bot_components.foto import Foto
from bot_components.gestore import add_message_handlers
from bot_components.insulti import Insulti
from bot_components.menu import init_menu
from bot_components.risposte import Risposte
from utils.os_utils import get_absolute_path


def main():
    load_dotenv()
    SERVER_PORT = get_server_port()
    is_server = 'ON_HEROKU' in environment_variables

    logging.basicConfig(level=logging.WARNING)

    BOT_TOKEN = environment_variables.get("BOT_TOKEN")
    BOT_TOKEN_LOCAL = environment_variables.get("BOT_TOKEN_LOCAL")

    updater = get_updater(BOT_TOKEN) if is_server else get_updater(BOT_TOKEN_LOCAL)
    dispatcher = updater.dispatcher

    setup_firebase()
    init_bot_components(dispatcher)

    if is_server:
        print("SERVER")
        updater.start_webhook(
            listen="0.0.0.0",
            port=SERVER_PORT,
            url_path=BOT_TOKEN,
            webhook_url=f'https://botvalo01.herokuapp.com/{BOT_TOKEN}'
        )
    else:
        print("LOCAL (testing)")
        updater.start_polling()
    updater.idle()


def get_server_port():
    return int(environment_variables.get('PORT', 8443))


def init_bot_components(dispatcher):
    logging.debug("Init components...")
    init_menu(dispatcher)
    Risposte.init()
    Insulti.init()
    Foto.init()
    add_message_handlers(dispatcher)
    logging.debug("Init done.")


def setup_firebase():
    path = get_absolute_path("botvalo_firebase_credentials.json")
    FirebaseApp.app = firebase_admin.initialize_app(Certificate(path))
    STORAGE_BUCKET_NAME = environment_variables["FIREBASE_BUCKET_NAME"]
    FirebaseApp.set_storage_bucket(STORAGE_BUCKET_NAME)


def get_updater(token: str) -> Updater:
    return Updater(token=token, use_context=True)


if __name__ == '__main__':
    main()
