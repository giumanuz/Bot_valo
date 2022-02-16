import logging
import unittest

from bot_components.foto import Foto, get_set_list
from bot_components.insulti import Insulti
from bot_components.menu import Menu
from bot_components.risposte import Risposte
from framework.mock_update_factory import MockUpdateFactory
from framework.mocks import *


# noinspection PyTypeChecker
class ConversationTests(unittest.TestCase):
    bot = MockBot()
    dispatcher = MockDispatcher(bot)
    context = MockContext(dispatcher)

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.DEBUG)

    def setUp(self):
        self.bot.reset_data()

    def test_Insulti_ifNonTriggerMessage_ShouldNotReply(self):
        res = self._send_fake_message_to(Insulti, "non_trigger")
        self.assertEqual(0, len(res))

    def test_Insulti_ifTriggerMessage_ShouldReplyWithInsult(self):
        res = self._send_fake_message_to(Insulti, "insulta")
        self.assertEqual(1, len(res))
        self.assertIn('text', res[0])
        self.assertIn(res[0].get('text')[7:], Insulti.lista_insulti)

    def test_Foto_ifTriggerWordSent_ShouldSendPhoto(self):
        for insieme in get_set_list():
            self.__testPhotoTriggerWord(next(iter(insieme)))

    def __testPhotoTriggerWord(self, word):
        res = self._send_fake_message_to(Foto, word)
        self.assertEqual(1, len(res))
        self.assertHasValidPhoto(res)
        self.bot.reset_data()

    def test_Foto_ifNonTriggerWordSent_ShouldNotSendPhoto(self):
        res = self._send_fake_message_to(Foto, "non_trigger")
        self.assertEqual(0, len(res))

    def test_onMenuCommand_ShouldSendMenu(self):
        from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
        update = MockUpdateFactory.empty()
        Menu.handle_command(update, self.context)
        res = self.bot.result

        self.assertEqual(1, len(res))
        self.assertIn('reply_markup', res[0])
        self.assertIsInstance(res[0]['reply_markup'], InlineKeyboardMarkup)

    def test_Risposte_ifTriggerWordSent_ShouldReply(self):
        res = self._send_fake_message_to(Risposte, "test")
        self.assertEqual(1, len(res))

    def test_Risposte_ifNonTriggerWordSent_ShouldNotReply(self):
        res = self._send_fake_message_to(Risposte, "non_trigger")
        self.assertEqual(0, len(res))

    def _send_fake_message_to(self, cls, text):
        update = MockUpdateFactory.with_message(text)
        cls.handle_message(update, self.context)
        return self.bot.result

    def assertHasValidPhoto(self, res):
        self.assertIn('photo', res[0])
        self.assertNotEqual(0, len(res[0]['photo']))


if __name__ == '__main__':
    unittest.main()
