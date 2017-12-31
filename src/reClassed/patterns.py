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

from reClassed import matched


class _MetaReClass(type):

    def __init__(cls, name, _bases, clsDict):
        # print("> __init__", cls, name)
        assert "match" in clsDict, "Pattern class {} requires field 'matchOn'".format(name)

        pattern = re.compile(cls.match)
        setattr(cls, "_pattern", pattern)
        setattr(cls, "_fill", _MetaReClass._compile_create(cls, clsDict, pattern))

    @staticmethod
    def _compile_create(cls, clsDict, pattern):
        # print("> _compile_create", cls, pattern)
        fillers = set()
        for name, element in clsDict.items():
            if isinstance(element, matched.MatchField):
                # print("## found", element, pattern)
                element.check(pattern)
                setattr(cls, name, element.fill)
                fillers.add((name, element.fill))

        def _do_create(self, string, mObj):
            for n, e in fillers:
                setattr(self, n, e(string, mObj))

        return _do_create


class ReClass(metaclass=_MetaReClass):
    _pattern = None
    _fill = None

    match = ""

    def __init__(self, string, mObj):
        # print("> __init__", self, string, mObj)
        self._fill(string, mObj)

    @classmethod
    def search(cls, string):
        mo = cls._pattern.search(string)
        return cls(string, mo) if mo else None


if __name__ == "__main__":
    pass
