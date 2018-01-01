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

from reClassed import matched, ReClass


class TestReClass(unittest.TestCase):

    class MyRe(ReClass):
        matchOn = "[abc]+([0-9]+)xy"
        no = matched.g1.asInt
        stuff = matched.g0

    def testGeneratedElements(self):
        cls = TestReClass.MyRe

        self.assertEqual(re.compile("[abc]+([0-9]+)xy"), cls._pattern)
        fields = cls._fields
        self.assertTrue(isinstance(fields, set))
        self.assertEqual({("no", matched.g1.asInt), ("stuff", matched.g0)}, fields)


class TestFieldsCheck(unittest.TestCase):

    def testInvalidGroup(self):
        with self.assertRaises(AssertionError):

            class NoCompile(ReClass):
                match = "my ([a-z]) is 1"
                field = matched.g2


if __name__ == '__main__':
    unittest.main()
