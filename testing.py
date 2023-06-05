import unittest
import calc


class TestAsyncLogger(unittest.TestCase):
    def test_add(self):
        result = 10+5
        self.assertEqual(result, 15)
