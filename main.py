import logging
from os import environ as environment_variables

from telegram.ext import Updater

from bot_components.foto import Foto
from bot_components.gestore import add_message_handlers
from bot_components.insulti import Insulti
from bot_components.menu import init_menu
from bot_components.risposte import Risposte

BOT_TOKEN = "5284256332:AAHv1djfMG6QQTobd-H_jUDpmsjvMgewpNM"
BOT_TOKEN_LOCAL = "5147856404:AAHdp2lv0mT_R2oF7BqWgANEGpSQaHiSvsI"


def main():
    SERVER_PORT = get_server_port()
    is_server = 'ON_HEROKU' in environment_variables

    logging.basicConfig(level=logging.WARNING)

    updater = get_updater(BOT_TOKEN) if is_server else get_updater(BOT_TOKEN_LOCAL)
    dispatcher = updater.dispatcher

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


def get_updater(token: str) -> Updater:
    return Updater(token=token, use_context=True)


if __name__ == '__main__':
    main()
