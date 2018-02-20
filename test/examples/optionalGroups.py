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


class NumericOrLogicId(ReWrap):
    """
    We want to match ids, which can be
        * just numbers,
        * alphanumeric expressions preceded by
            * "id"
            * the @ symbol
    
    This makes three groups, and we will always either
    match the first one only, or both the second and third.

    TODO: add differing space for id and @, and trim that out
         in the definition of the fields:
        ((?:id\s+|@\s*)(([0-9a-zA-Z]+)))
        
        idTag = matched.g2.trim
    """
    matchOn = "([0-9]+)|(id|@)\s+([0-9a-zA-Z]+)"

    numId = matched.gOr(1, -1).asInt
    idTag = matched.g2
    alphaNumId = matched.g3


class TestSomeGroups(unittest.TestCase):

    def testSimple(self):
        res = NumericOrLogicId.findall("item 777, then @ a76, then id 777 and 123")
        self.assertEqual(4, len(res))
        r = res[0]
        self.assertEqual((777, None, None), (r.numId, r.idTag, r.alphaNumId))
        r = res[1]
        self.assertEqual((-1, "@", "a76"), (r.numId, r.idTag, r.alphaNumId))
        r = res[2]
        self.assertEqual((-1, "id", "777"), (r.numId, r.idTag, r.alphaNumId))
        r = res[3]
        self.assertEqual((123, None, None), (r.numId, r.idTag, r.alphaNumId))


class NumericOrLogicIdWithBreak(ReWrap):
    matchOn = "([0-9]+)|(id|@)\s+([0-9a-zA-Z]+)"

    numId = matched.g1.breakOnNone.asInt
    idTag = matched.g2
    alphaNumId = matched.g3


class TestGroupsWithBreak(unittest.TestCase):

    def testSimple(self):
        res = NumericOrLogicIdWithBreak.findall("item 777, then @ a76, then id 777 and 123")
        self.assertEqual(4, len(res))
        r = res[0]
        self.assertEqual((777, None, None), (r.numId, r.idTag, r.alphaNumId))
        r = res[1]
        self.assertEqual((None, "@", "a76"), (r.numId, r.idTag, r.alphaNumId))
        r = res[2]
        self.assertEqual((None, "id", "777"), (r.numId, r.idTag, r.alphaNumId))
        r = res[3]
        self.assertEqual((123, None, None), (r.numId, r.idTag, r.alphaNumId))


if __name__ == '__main__':
    unittest.main()
