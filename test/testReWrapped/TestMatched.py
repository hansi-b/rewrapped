# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""

__author__ = "Hans Bering"
__copyright__ = "Copyright 2018"
__credits__ = ["Hans Bering"]
__license__ = "MIT License"
__maintainer__ = "Hans Bering"
__email__ = "hansi.b.github@moc.liamg"
__status__ = "Development"

"""

import unittest
from reWrapped.matched import MatchField
from reWrapped.patterns import ReWrap


class TestIncompleteField(unittest.TestCase):

    def testMissingCheckMethod(self):
        """
        Already fails when a ReWrap class is constructed.
        """

        class MissingCheckField(MatchField):
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
 
if __name__ == "__main__":
    unittest.main()
