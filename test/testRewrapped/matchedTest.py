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

from rewrapped import matched


class TestGroupCall(unittest.TestCase):

    def testGroupZero(self):
        g = matched.group()
        self.assertIsInstance(g, matched._Group)
        self.assertEquals(0, g._index)

    def testSingleGroup(self):
        g = matched.group(1)
        self.assertIsInstance(g, matched._Group)
        self.assertEquals(1, g._index)

    def testMultipleGroups(self):
        g = matched.group(1, 2)
        self.assertIsInstance(g, matched._GroupTuple)
        self.assertEquals((1, 2), g._indices)
