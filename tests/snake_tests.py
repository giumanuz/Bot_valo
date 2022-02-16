import unittest

from bot_components.games.snake import Snake
from tests.framework.mocks import MockBot, MockDispatcher, MockContext


class SnakeTests(unittest.TestCase):
    bot = MockBot()
    dispatcher = MockDispatcher(bot)
    context = MockContext(dispatcher)

    def test_nothing(self):
        snake = Snake()


if __name__ == '__main__':
    unittest.main()
