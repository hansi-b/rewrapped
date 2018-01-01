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
        assert "match" in clsDict, "Pattern class {} requires field 'match'".format(name)

        pattern = re.compile(cls.match)
        setattr(cls, "_pattern", pattern)
        setattr(cls, "_fields", _MetaReClass._get_fields(cls, clsDict, pattern))

    @staticmethod
    def _get_fields(cls, clsDict, pattern):
        fields = set()
        for name, element in clsDict.items():
            if isinstance(element, matched.MatchField):
                # print("## found", element, pattern)
                element.check(pattern)
                fields.add((name, element.fill))

        return fields


class ReClass(metaclass=_MetaReClass):
    _pattern = None
    _fields = None

    match = ""

    def __init__(self, string, mObj):
        for n, e in self._fields:
            setattr(self, n, e(string, mObj))

    @classmethod
    def search(cls, string):
        mo = cls._pattern.search(string)
        return cls(string, mo) if mo else None


if __name__ == "__main__":
    pass
