import logging
import unittest

from bot_components.foto import Foto, get_set_list
from bot_components.insulti import Insulti
from framework.mocks import *


# noinspection PyTypeChecker
class ConversationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.DEBUG)

    def setUp(self):
        self.bot = MockBot()
        self.dispatcher = MockDispatcher(self.bot)
        self.context = MockContext(self.dispatcher)

    def test_Insulti_ifNonTriggerMessage_ShouldNotReply(self):
        update = self.__create_update("nontrigger_message")
        Insulti.handle_message(update, self.context)
        self.assertEqual(0, len(self.bot.result))

    def test_Insulti_ifTriggerMessage_ShouldReplyWithInsult(self):
        update = self.__create_update("insulta")
        Insulti.handle_message(update, self.context)
        res = self.bot.result
        self.assertEqual(1, len(res))
        self.assertIn('text', res[0])
        self.assertIn(res[0].get('text')[7:], Insulti.lista_insulti)

    def test_Foto_ifTriggerWordSent_ShouldSendPhoto(self):
        for insieme in get_set_list():
            self.__testPhotoTriggerWord(next(iter(insieme)))

    def __testPhotoTriggerWord(self, word):
        update = self.__create_update(word)
        Foto.handle_message(update, self.context)
        res = self.bot.result
        self.assertEqual(1, len(res))
        self.assertHasValidPhoto(res)
        self.bot.reset_data()

    def assertHasValidPhoto(self, res):
        self.assertIn('photo', res[0])
        self.assertNotEqual(0, len(res[0]['photo']))

    def test_Foto_ifNonTriggerWordSent_ShouldNotSendPhoto(self):
        update = self.__create_update("nontrigger_word")
        Foto.handle_message(update, self.context)
        res = self.bot.result
        self.assertEqual(0, len(res))

    @staticmethod
    def __create_update(message) -> MockUpdate:
        return MockUpdate(MockMessage(message))


if __name__ == '__main__':
    unittest.main()
