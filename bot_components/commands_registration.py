from telegram.ext import Dispatcher


class CommandRegister:
    _commands: list[tuple[str, str]] = []
    _dispatcher: Dispatcher

    @classmethod
    def register_command(cls, command: str, description: str):
        cls._commands.append((command, description))

    @classmethod
    def init(cls, dispatcher):
        cls._dispatcher = dispatcher

    @classmethod
    def update_commands(cls):
        cls._dispatcher.bot.set_my_commands(cls._commands)
