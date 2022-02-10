import logging
import unittest

from bot_components.insulti import Insulti
from framework.mocks import *


class ConversationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.DEBUG)
        Insulti.initialize()

    def setUp(self):
        self.bot = MockBot()
        self.dispatcher = MockDispatcher(self.bot)
        self.context = MockContext(self.dispatcher)

    def test_Insulti_ifNonTriggerMessage_ShouldNotReply(self):
        update = self.__create_update("nontrigger_message")
        Insulti.command_handler_insulti(update, self.context)
        self.assertEqual(len(self.bot.result), 0)

    def test_Insulti_ifTriggerMessage_ShouldReplyWithInsult(self):
        update = self.__create_update("insulta")
        Insulti.command_handler_insulti(update, self.context)
        res = self.bot.result
        self.assertEqual(len(res), 1)
        self.assertIsInstance(res[0], dict)
        self.assertIn('text', res[0])
        self.assertIn(res[0].get('text')[7:], Insulti.lista_insulti)

    @staticmethod
    def __create_update(message) -> MockUpdate:
        return MockUpdate(MockMessage(message))


if __name__ == '__main__':
    unittest.main()
