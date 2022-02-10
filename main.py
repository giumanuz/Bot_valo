import logging
from os import environ as environment_variables

from telegram.ext import Updater

from bot_component.gestore import Gestore
from bot_component.menu import init_menu
from bot_component.tris import init_tris


def main():
    SERVER_PORT = int(environment_variables.get('PORT', 8443))
    BOT_TOKEN = "5284256332:AAHv1djfMG6QQTobd-H_jUDpmsjvMgewpNM"

    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    logging.debug("Init components...")
    init_menu(dispatcher)
    init_tris(dispatcher)
    Gestore.init(dispatcher)
    logging.debug("Init done.")

    if 'ON_HEROKU' in environment_variables:
        print("SERVER")
        updater.start_webhook(
            listen="0.0.0.0",
            port=SERVER_PORT,
            url_path=BOT_TOKEN,
            webhook_url=f'https://botvalo01.herokuapp.com/{BOT_TOKEN}'
        )
    else:
        print("LOCAL")
        updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
