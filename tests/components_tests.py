from bot_components.menu import Menu
from tests.framework.mockdispatcher import MockDispatcher


def test_Menu_shouldAddCommandHandler_WhenInit():
    from telegram.ext import CommandHandler
    d = MockDispatcher(None)
    Menu.init(d)
    assert len(d.handlers) == 1
    ch: CommandHandler = d.handlers[0]
    assert isinstance(ch, CommandHandler)
    assert ch.command[0] == "menu"
    assert ch.callback == Menu.show
