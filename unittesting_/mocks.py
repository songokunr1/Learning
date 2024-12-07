# https://myadventuresincoding.wordpress.com/2011/02/26/python-python-mock-cheat-sheet/
def a():
    return False
def b():
    return False

import unittest
from unittest.mock import Mock, patch
from app.api import calc

class TestApi(unittest.TestCase):
    # @patch('app.api.outer')
    @patch('app.api.outer')
    def test(self, outer):
        mc = outer.return_value
        mc.a.return_value = 1
        result = calc()
        self.assertEqual(1, result)


if __name__ == '__main__':
    unittest.main()

