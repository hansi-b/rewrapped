# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""

__author__ = "Hans Bering"
__copyright__ = "Copyright 2018"
__credits__ = ["Hans Bering"]
__license__ = "MIT License"
__maintainer__ = "Hans Bering"
__email__ = "hansi.b.github@mgail.moc"
__status__ = "Development"

"""

import unittest

from reWrapped import ReWrap, matched


class SomeGroups(ReWrap):
    matchOn = "(a)?,(b*),(c?),(d+)"

    all = matched.gTuple(1, 2, 3, 4)


class TestSomeGroups(unittest.TestCase):

    def testSimple(self):
        res = SomeGroups.search("Found a,bb,c,dddd")
        self.assertEqual(('a', 'bb', 'c', 'dddd'), res.all)


if __name__ == '__main__':
    unittest.main()
