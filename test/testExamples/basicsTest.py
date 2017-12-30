# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""

__author__ = "Hans Bering"
__copyright__ = "Copyright 2017"
__credits__ = ["Hans Bering"]
__license__ = "MIT License"
__maintainer__ = "Hans Bering"
__email__ = "hansi.b.github@mgail.moc"
__status__ = "Development"

"""

import unittest

from reClassed.patterns import ReClass
from reClassed import matched


class Number(ReClass):
    match = "Number ([0-9]+)"
    no = matched.g1.asInt


class NumberTest(unittest.TestCase):

    def testSearch(self):
        res = Number.search("Number 11 came up")

        self.assertTrue(isinstance(res, Number))
        self.assertEqual(11, res.no)

    def testSearchNoMatch(self):
        res = Number.search("Number x came up")
        self.assertIsNone(res)


class MatchedTest(unittest.TestCase):

    def testInvalidGroup(self):
        with self.assertRaises(AssertionError):
            class NoCompile(ReClass):
                match = "my ([a-z]) is 1"
                field = matched.g2


if __name__ == '__main__':
    unittest.main()
