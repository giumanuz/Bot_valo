from bot_component.tris import init_tris
from bot_component.menu import init_menu
from bot_component.insulti import init_insulti
from bot_component.risposte import init_risposte
from bot_component.foto import init_foto
from os import environ as environment_variables
from telegram.ext import Updater


def main():
    SERVER_PORT = int(environment_variables.get('PORT', 8443))
    # Should NOT be hardcoded here
    BOT_TOKEN = "5284256332:AAHv1djfMG6QQTobd-H_jUDpmsjvMgewpNM"

    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    init_menu(dispatcher)
    init_tris(dispatcher)
    init_foto(dispatcher)
    init_risposte(dispatcher)
    init_insulti(dispatcher)

    if 'ON_HEROKU' in environment_variables:
        print("SERVER")

        updater.start_webhook(listen="0.0.0.0",
                              port=SERVER_PORT,
                              url_path=BOT_TOKEN,
                              webhook_url=f'https://botvalo01.herokuapp.com/{BOT_TOKEN}')
    else:
        print("LOCAL")

        updater.start_polling()
    updater.idle()
    pass


if __name__ == '__main__':
    main()
