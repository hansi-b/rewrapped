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
    matchOn = "([0-9]+)"
    no = matched.g1.asInt


class TestSearchWithPos(unittest.TestCase):

    def testStartPosSearch(self):
        res = AnInt.search("and Number 123 came up", pos=4)
        self.assertEqual(123, res.no)

    def testStartPosNoSearch(self):
        s = "now 1234 is up"
        assert "1234" == s[4:8]

        res = AnInt.search(s, pos=5)
        self.assertEqual(234, res.no)

    def testStartAndEndPosSearch(self):
        s = "now 1234 is up"
        assert "1234" == s[4:8]

        res = AnInt.search(s, endpos=7)
        self.assertEqual(123, res.no)

    def testStartAndEndPosNoSearch(self):
        s = "and Number 789 came up"
        assert "789" == s[11:14]
        res = AnInt.search(s, pos=4, endpos=13)
        self.assertEqual(78, res.no)


class NumberWithInt(ReWrap):
    matchOn = "Number ([0-9]+)"
    no = matched.g1.asInt


class TestMatch(unittest.TestCase):

    def testMatch(self):
        res = NumberWithInt.match("Number 11 came up")
        self.assertEqual(11, res.no)

    def testNoMatch(self):
        self.assertIsNone(AnInt.match("and Number 11 did not"))

    def testStartPosMatch(self):
        res = NumberWithInt.match("and Number 12 came up", pos=4)
        self.assertEqual(12, res.no)

    def testStartPosNoMatch(self):
        self.assertIsNone(NumberWithInt.match("and Number 11 did not", pos=3))
        self.assertIsNone(NumberWithInt.match("and Number 11 did not", pos=5))

    def testStartAndEndPosMatch(self):
        res = NumberWithInt.match("and Number 144 came up", pos=4, endpos=15)
        self.assertEqual(144, res.no)

    def testStartAndEndPosNoMatch(self):
        s = "and Number 789 came up"
        assert "789" == s[11:14]
        res = NumberWithInt.match(s, pos=4, endpos=13)
        self.assertEqual(78, res.no)


class TestFullMatch(unittest.TestCase):

    def testNoMatch(self):
        self.assertIsNone(AnInt.fullmatch("Number 11 came up"))

    def testStartPosMatch(self):
        res = NumberWithInt.fullmatch("and Number 12", pos=4)
        self.assertEqual(12, res.no)

    def testStartPosNoMatch(self):
        self.assertIsNone(NumberWithInt.fullmatch("and Number 11", pos=3))
        self.assertIsNone(NumberWithInt.fullmatch("and Number 11", pos=5))

    def testStartAndEndPosMatch(self):
        s = "and Number 144 came up"
        assert "Number 144" == s[4:14]
        res = NumberWithInt.fullmatch(s, pos=4, endpos=14)
        self.assertEqual(144, res.no)

    def testStartAndEndPosNoMatch(self):
        s = "and Number 144 came up"
        res = NumberWithInt.fullmatch(s, pos=4, endpos=13)
        self.assertEqual(14, res.no)


class TestFindIter(unittest.TestCase):

    def testNoMatches(self):
        resIter = NumberWithInt.finditer("no Number came up")
        with self.assertRaises(StopIteration):
            next(resIter)

    def testSomeMatches(self):
        resIter = NumberWithInt.finditer("first Number 57, then Number 12 came up, and finally Number 32")
        self.assertEqual(57, next(resIter).no)
        self.assertEqual(12, next(resIter).no)
        self.assertEqual(32, next(resIter).no)
        with self.assertRaises(StopIteration):
            next(resIter)


if __name__ == '__main__':
    unittest.main()
