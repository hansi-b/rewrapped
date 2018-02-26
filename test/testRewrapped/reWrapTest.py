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

import re
import unittest

from rewrapped import matched, ReWrap
from rewrapped.patterns import MatchField


class TestIncompleteField(unittest.TestCase):

    def testMissingCheckMethod(self):

        class MissingCheckField(MatchField):
            """
            Causes a failure when used in a ReWrap class when
            that class is constructed.
            """
            pass

        with self.assertRaises(NotImplementedError) as errCtxt:

            class SomeNewPattern(ReWrap):
                matchOn = "Hello check method"
                aField = MissingCheckField()

        self.assertEqual("MissingCheckField requires method 'check'", str(errCtxt.exception))

    def testMissingFillMethod(self):
        """
        Only fails at match time.
        """

        class MissingFillField(MatchField):
            
            def check(self, pattern):
                pass

        class AnotherNewPattern(ReWrap):
            matchOn = "Hello fill method"
            aField = MissingFillField()

        with self.assertRaises(NotImplementedError) as errCtxt:
            AnotherNewPattern.search("Hello fill method")
        self.assertEqual("MissingFillField requires method 'fill'", str(errCtxt.exception))


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
        assert len(fields) == 4
        assert {"optFinally", "no", "allOfIt", "theAlphas"} == set(p[0] for p in fields)


class TestFieldsCheck(unittest.TestCase):

    def testMissingMatchOn(self):
        with self.assertRaisesRegex(AssertionError,
                                    "ReWrap MissingMatchOn requires field 'matchOn'"):

            class MissingMatchOn(ReWrap):
                match = "my ([a-z]) is x"
                field = matched.g1

    def testInvalidGroup(self):
        with self.assertRaisesRegex(AssertionError,
                                    "Pattern .+ has 1 group\(s\) \(got group index 2\)"):

            class ReInvalidGroup(ReWrap):
                matchOn = "my ([a-z]) is x"
                field = matched.g2


class TestMatchOnTupleCheck(unittest.TestCase):

    def testMatchWithFlags(self):

        class IgnoreCase(ReWrap):
            matchOn = "\w+", re.IGNORECASE | re.MULTILINE  # @UndefinedVariable
            word = matched.g0
        
        self.assertEquals(re.compile('\\w+', re.IGNORECASE | re.MULTILINE),  # @UndefinedVariable
                          IgnoreCase._pattern)

    def testInvalidTuple(self):
        with self.assertRaises(AssertionError):

            class IgnoreCase(ReWrap):
                matchOn = "\w+", re.IGNORECASE, re.MULTILINE  # @UndefinedVariable
                word = matched.g0


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
        for vs in 'anInt=-1 optFloat=0.33 aToZ="first"'.split():
            self.assertTrue(vs in r, msg="Missing '{}' in {}".format(vs, r))


if __name__ == '__main__':
    unittest.main()
