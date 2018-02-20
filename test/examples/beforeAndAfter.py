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


class Parts(ReWrap):
    matchOn = "\s*([a-z]+),\s*"

    whole = matched.g0
    part = matched.g1

    before = matched.before
    after = matched.after


class TestBeforeAndAfter(unittest.TestCase):

    def testSearch(self):
        res = Parts.search("first oranges, then")

        self.assertEqual(" oranges, ", res.whole)
        self.assertEqual("oranges", res.part)

        self.assertEqual("first", res.before)
        self.assertEqual("then", res.after)


if __name__ == '__main__':
    unittest.main()
