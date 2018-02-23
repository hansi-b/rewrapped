# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
"""

__author__ = "Hans Bering"
__copyright__ = "Copyright 2018"
__credits__ = ["Hans Bering"]
__license__ = "MIT License"
__maintainer__ = "Hans Bering"
__email__ = "hansi.b.github@moc.liamg"
__status__ = "Development"

import unittest
import re

from rewrapped.modders import SingleValueField, TupleValueField
from rewrapped.patterns import MatchField


class TestTupleValueField(unittest.TestCase):

    def testAsFloats(self):
        
        # cheap mock of a 1,2-Groups field
        g12 = MatchField()
        g12.fill = lambda _s, mo: (mo.group(1), mo.group(2))

        tvf = TupleValueField(g12).asFloats
        
        matchObject = re.search("(1\.[0-9]+)\+(2\.[0-9]+)", "1.123+2.2314")
        assert (1.123, 2.2314) == tvf.fill(None, matchObject)

class TestEqualities(unittest.TestCase):

    def testSingleValueField(self):
        
        assert SingleValueField('A').asInt == SingleValueField('A').asInt
        assert SingleValueField('A').asInt != SingleValueField('B').asInt
        assert SingleValueField('A').asInt != SingleValueField('B').asFloat

    def testBreakOn(self):
        
        assert SingleValueField('A').breakOn(1) == SingleValueField('A').breakOn(1)
        assert SingleValueField('A').breakOn(1) != SingleValueField('B').breakOn(1)
        assert SingleValueField('A').breakOn(1) != SingleValueField('A').breakOn(2)

    def testTupleValueField(self):
        
        assert TupleValueField('A').asInts == TupleValueField('A').asInts
        assert TupleValueField('A').asInts != TupleValueField('B').asInts
        assert TupleValueField('A').asInts != TupleValueField('B').asFloats
