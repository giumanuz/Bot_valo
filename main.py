import logging
from os import environ as environment_variables

from dotenv import load_dotenv
from telegram.ext import Updater

from bot_components.anti_cioppy_policy import AntiCioppyPolicy
from bot_components.commands.bancioppy_command import BanCioppyCommand
from bot_components.db.db_manager import Database
from bot_components.db.firebase_manager import FirebaseStorage
from bot_components.foto import Foto
from bot_components.games.snake import init_snake
from bot_components.games.tris import init_tris
from bot_components.gestore import add_message_handlers
from bot_components.insulti import Insulti
from bot_components.menu import Menu
from bot_components.prenotazioni import init_prenotazioni
from bot_components.risposte import Risposte
from bot_components.settings.settings import ChatSettings


def main():
    load_dotenv()
    SERVER_PORT = get_server_port()
    is_server = 'ON_HEROKU' in environment_variables

    check_environment_variables(is_server)

    logging.basicConfig(level=logging.WARNING)

    BOT_TOKEN = environment_variables.get("BOT_TOKEN")
    BOT_TOKEN_LOCAL = environment_variables.get("BOT_TOKEN_LOCAL")

    updater = get_updater(BOT_TOKEN) if is_server else get_updater(BOT_TOKEN_LOCAL)
    dispatcher = updater.dispatcher

    setup_db()
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


def check_environment_variables(is_server):
    required_envs = ("FB_PROJECT_ID",
                     "FB_CREDENTIALS_KEY_ID",
                     "FB_CREDENTIALS_PRIVATE_KEY",
                     "FB_CLIENT_EMAIL",
                     "FB_CLIENT_ID",
                     "FB_BUCKET_NAME",
                     "BOT_TOKEN" if is_server else "BOT_TOKEN_LOCAL")
    error = False
    for env in required_envs:
        if env not in environment_variables:
            logging.critical(f"Missing required environment variable: {env}")
            error = True
    if error:
        exit(ExitCode.MISSING_REQUIRED_ENV)


def setup_db():
    Database.set_db_type(FirebaseStorage)
    FirebaseStorage.init()


def init_bot_components(dispatcher):
    logging.info("Init components...")

    Menu.init(dispatcher)
    BanCioppyCommand.init(dispatcher)
    init_prenotazioni(dispatcher)
    init_tris(dispatcher)
    init_snake(dispatcher)
    ChatSettings.init(dispatcher)

    Risposte.init()
    Insulti.init()
    Foto.init()
    AntiCioppyPolicy.init()

    add_message_handlers(dispatcher)

    logging.info("Init done.")


def get_updater(token: str) -> Updater:
    return Updater(token=token, use_context=True)


class ExitCode:
    OK = 0
    UNKNOWN_ERROR = 1
    MISSING_REQUIRED_ENV = 2


if __name__ == '__main__':
    main()
