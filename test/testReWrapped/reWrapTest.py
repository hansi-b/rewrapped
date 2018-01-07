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
import re
import unittest

from reWrapped import matched, ReWrap


class TestReClass(unittest.TestCase):

    class MyRe(ReWrap):
        matchOn = "([0-9]+) ([abc]+) xy (finally)?"
        optFinally = matched.gOr(3, "nope")
        no = matched.g1.asInt
        allOfIt = matched.g0
        theAlphas = matched.g2

    def testGeneratedElements(self):
        """
            Starting with Python 3.6, this could also check for ordering of
            fields.
        """
        cls = TestReClass.MyRe

        self.assertEqual(re.compile("([0-9]+) ([abc]+) xy (finally)?"), cls._pattern)
        fields = cls._fields
        self.assertTrue(isinstance(fields, tuple))
        self.assertEqual({("optFinally", matched.gOr(3, "nope")),
                          ("no", matched.g1.asInt),
                          ("allOfIt", matched.g0),
                          ("theAlphas", matched.g2)},
                         set(fields))


class TestFieldsCheck(unittest.TestCase):

    def testInvalidGroup(self):
        with self.assertRaises(AssertionError):

            class MissingMatchOn(ReWrap):
                match = "my ([a-z]) is 1"
                field = matched.g2


class TestRepr(unittest.TestCase):

    class SomeMatchFields(ReWrap):
        matchOn = "([0-9])+ |([a-z]+) ([0-9]*\.[0-9]+)?"
        anInt = matched.gOr(1, -1).asInt
        optFloat = matched.gOr(3, 0).asFloat
        aToZ = matched.g2
        
    def testNumAndNoneGroup(self):
        
        r = repr(TestRepr.SomeMatchFields.search("123 first"))
        self.assertTrue(r.startswith("SomeMatchFields("))
        # cannot check for order here if we want to allow Python < 3.6
        for vs in "anInt=3 optFloat=0.0 aToZ=None".split():
            self.assertTrue(vs in r, msg="Missing '{}' in {}".format(vs, r))

    def testQuotedGroup(self):
        
        r = repr(TestRepr.SomeMatchFields.search("first 0.33"))
        self.assertTrue(r.startswith("SomeMatchFields("))
        # cannot check for order here if we want to allow Python < 3.6
        for vs in "anInt=-1 optFloat=0.33 aToZ=\"first\"".split():
            self.assertTrue(vs in r, msg="Missing '{}' in {}".format(vs, r))


if __name__ == '__main__':
    unittest.main()
