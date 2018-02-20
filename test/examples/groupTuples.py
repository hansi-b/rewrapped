# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
"""

__author__ = "Hans Bering"
__copyright__ = "Copyright 2018"
__credits__ = ["Hans Bering"]
__license__ = "MIT License"
__maintainer__ = "Hans Bering"
__email__ = "hansi.b.github@mgail.moc"
__status__ = "Development"

import unittest

from rewrapped import ReWrap, matched


class SomeGroups(ReWrap):
    matchOn = "(a)?,(b*),(c?),(d+)"

    allListed = matched.gTuple(1, 2, 3, 4)
    noneListed = matched.gTuple()


class TestSomeGroups(unittest.TestCase):

    def testAllTuples(self):
        res = SomeGroups.search("Found a,bb,c,dddd")
        self.assertEqual(('a', 'bb', 'c', 'dddd'), res.allListed)
        self.assertEqual(('a', 'bb', 'c', 'dddd'), res.noneListed)


class NumberGroups(ReWrap):
    matchOn = "(3)?,(5*),(7?),(9+)"

    twoStrings = matched.gTuple(1, 3)
    twoInts = matched.gTuple(2, 4).asInts


class TestNumberGroups(unittest.TestCase):

    def testTuplesConvert(self):
        res = NumberGroups.search("Found 3,55,7,99")
    
        self.assertEqual(("3", "7"), res.twoStrings)
        self.assertEqual((55, 99), res.twoInts)


import datetime


class TupleApply(ReWrap):
    matchOn = "started ([0-9]{4})-([0-9]{2})-([0-9]{2})"

    started = matched.gTuple().asInts.apply(datetime.datetime)


class TestTupleConvert(unittest.TestCase):

    def testTuplesConvert(self):
        res = TupleApply.search("started 1999-12-14")
    
        self.assertEqual(datetime.datetime(1999, 12, 14), res.started)


if __name__ == '__main__':
    unittest.main()
