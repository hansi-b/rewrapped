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


class SomeGroups(ReWrap):
    matchOn = "(a)?,(b*),(c?),(d+)"

    all = matched.g0
    anA = matched.g1
    someBs = matched.g2
    perhapsC = matched.g3
    someDs = matched.g(4)


class TestSomeGroups(unittest.TestCase):

    def testSimple(self):
        res = SomeGroups.search("Found a,bb,c,dddd")

        self.assertTrue(isinstance(res, SomeGroups))
        self.assertEqual('a,bb,c,dddd', res.all)
        self.assertEqual('a', res.anA)
        self.assertEqual('bb', res.someBs)
        self.assertEqual('c', res.perhapsC)
        self.assertEqual('dddd', res.someDs)

    def testOptionals(self):
        res = SomeGroups.search("... aaand now ,,,ddd")

        self.assertTrue(isinstance(res, SomeGroups))
        
        self.assertEqual(',,,ddd', res.all)
        self.assertEqual(None, res.anA)
        self.assertEqual('', res.someBs)
        self.assertEqual('', res.perhapsC)
        self.assertEqual('ddd', res.someDs)


class SimpleApplyRe(ReWrap):
    matchOn = "(\w+)"

    number = matched.g1.apply(lambda v:v + "x")


class TestSimpleConvert(unittest.TestCase):

    def testSearch(self):
        res = SimpleApplyRe.search("123 house")

        self.assertEqual("123x", res.number)


class SimpleOptionalRe(ReWrap):
    matchOn = "[a-z ]+([0-9]+)?"

    number = matched.gOr(1, 42).asInt


class TestSimpleOptional(unittest.TestCase):

    def testSearch(self):
        res = SimpleOptionalRe.search("house 123")
        self.assertEqual(123, res.number)

        res = SimpleOptionalRe.search("house")
        self.assertEqual(42, res.number)


class DateRe(ReWrap):
    matchOn = "on ([0-9]{4})\-([0-9]{2})\-([0-9]{2})"

    year = matched.g1.asInt
    month = matched.g2.asInt
    day = matched.g3.asInt

    def asDate(self):
        import datetime
        return datetime.datetime(self.year, self.month, self.day)


class TestDateRe(unittest.TestCase):

    def testSearch(self):
        res = DateRe.search("on 2017-04-12")

        import datetime
        dt = datetime.datetime(2017, 4, 12)
        self.assertEqual(dt, res.asDate())


class StrippingRe(ReWrap):
    matchOn = "(\s+\S+\s+)"

    word = matched.g1.strip


class TestStripping(unittest.TestCase):

    def testSearch(self):
        res = StrippingRe.search("first house 123")
        self.assertEqual("house", res.word)


if __name__ == '__main__':
    unittest.main()
