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


class SomeGroups(ReClass):
    match = "(1)?,(2*),(3?),(4+)"
    all = matched.g0
    ones = matched.g1.asInt
    twos = matched.g2.asInt
    threes = matched.g3.asInt
    fours = matched.g(4).asInt


class SomeGroupsTest(unittest.TestCase):

    def testSimple(self):
        res = SomeGroups.search("Numbers 1,22,3,444")

        self.assertTrue(isinstance(res, SomeGroups))
        self.assertEqual('1,22,3,444', res.all)
        self.assertEqual(1, res.ones)
        self.assertEqual(22, res.twos)
        self.assertEqual(3, res.threes)
        self.assertEqual(444, res.fours)

    def testOptionals(self):
        res = SomeGroups.search("Numbers ,,,444")

        self.assertTrue(isinstance(res, SomeGroups))
        
        self.assertEqual(',,,444', res.all)
        self.assertEqual(None, res.ones)
        self.assertEqual('', res.twos)
        self.assertEqual('', res.threes)
        self.assertEqual(444, res.fours)


class MatchedTest(unittest.TestCase):

    def testInvalidGroup(self):
        with self.assertRaises(AssertionError):

            class NoCompile(ReClass):
                match = "my ([a-z]) is 1"
                field = matched.g2


if __name__ == '__main__':
    unittest.main()
