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
from rewrapped.patterns import ReWrap


class TestWrapNoneInSubclass(unittest.TestCase):

    class OneGroup(ReWrap):
        matchOn = "(abc)"
        wrapNone = True

        abc = matched.g1

    class AnotherGroup(ReWrap):
        matchOn = "(abc)"
        abc = matched.g0

    def testWrapNoneTrueInOneSubclassButNotAnother(self):

        ReWrap.wrapNone = False # just to make sure

        gOne = TestWrapNoneInSubclass.OneGroup.search("xyz")
        assert gOne is not None

        gAnother = TestWrapNoneInSubclass.AnotherGroup.search("xyz")
        assert gAnother is None

class TestWrapNoneThroughBaseClass(unittest.TestCase):

    class FirstGroup(ReWrap):
        matchOn = "(abc)"
        abc = matched.g1

    def testWrapNoneTrueInBaseClass(self):

        ReWrap.wrapNone = True

        gOne = TestWrapNoneThroughBaseClass.FirstGroup.search("xyz")
        assert gOne is not None

        ReWrap.wrapNone = False # just to make sure
