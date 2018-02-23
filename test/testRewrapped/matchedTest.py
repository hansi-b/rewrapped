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
        self.assertEquals(matched.g(0), g)

    def testSingleGroup(self):
        g = matched.group(1)
        self.assertEquals(matched.g(1), g)

    def testMultipleGroups(self):
        g = matched.group(1, 2)
        self.assertEquals(matched.gTuple(1, 2), g)
