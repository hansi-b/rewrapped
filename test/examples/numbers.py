# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
"""

__author__ = "Hans Bering"
__copyright__ = "Copyright 2017"
__credits__ = ["Hans Bering"]
__license__ = "MIT License"
__maintainer__ = "Hans Bering"
__email__ = "hansi.b.github@mgail.moc"
__status__ = "Development"

import unittest

from rewrapped import ReWrap, matched


class AnInt(ReWrap):
    matchOn = "Number ([0-9]+)"
    no = matched.g1.asInt


class TestAsInt(unittest.TestCase):

    def testSearch(self):
        res = AnInt.search("Number 11 came up")

        self.assertEqual(11, res.no)

    def testSearchNoMatch(self):
        res = AnInt.search("Number x came up")
        self.assertIsNone(res)


class Floater(ReWrap):
    matchOn = "beyond ([+-]?[0-9]+\.[0-9]+)"
    limit = matched.g1.asFloat


class TestAsFloat(unittest.TestCase):

    def testSearch(self):
        res = Floater.search("beyond 11.01")

        self.assertEqual(11.01, res.limit)

    def testSearchNoMatch(self):
        res = Floater.search("beyond 23")
        self.assertIsNone(res)


if __name__ == '__main__':
    unittest.main()
