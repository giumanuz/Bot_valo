import unittest

from bot_components.tris import Tris


class TrisTests(unittest.TestCase):
    def setUp(self):
        self.tris = Tris()


if __name__ == '__main__':
    unittest.main()
