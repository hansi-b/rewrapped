# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
"""
from rewrapped.modders import SingleValueField, TupleValueField

__author__ = "Hans Bering"
__copyright__ = "Copyright 2018"
__credits__ = ["Hans Bering"]
__license__ = "MIT License"
__maintainer__ = "Hans Bering"
__email__ = "hansi.b.github@moc.liamg"
__status__ = "Development"

import unittest

from rewrapped import matched


class TestGroupCall(unittest.TestCase):

    def testGroupZero(self):
        g = matched.group()
        assert isinstance(g, SingleValueField)
        assert g._origin._index == 0

    def testSingleGroup(self):
        g = matched.group(1)
        assert isinstance(g, SingleValueField)
        assert g._origin._index == 1

    def testMultipleGroups(self):
        g = matched.group(1, 2)
        assert isinstance(g, TupleValueField)
        assert g._origin._indices == (1,2)
