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
import types
import unittest

from reClassed.patterns import ReClass
from reClassed import matched


class ReClassTest(unittest.TestCase):
    class MyPattern(ReClass):
        match = "[abc]+([0-9]+)xy"
        no = matched.g1.asInt

    def testGeneratedElements(self):
        cls = ReClassTest.MyPattern

        self.assertEqual(re.compile("[abc]+([0-9]+)xy"), cls._pattern)
        self.assertTrue(isinstance(cls._fill, types.FunctionType))


if __name__ == '__main__':
    unittest.main()
