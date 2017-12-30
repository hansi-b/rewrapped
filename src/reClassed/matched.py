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


class _Matchable:
    def check(self, pattern):
        raise NotImplementedError("{} requires method '{}'".format(self.__class__.__name__,
                                                                   _Matchable.check.__name__))

    def fill(self, matchObject):
        raise NotImplementedError("{} requires method '{}'".format(self.__class__.__name__,
                                                                   _Matchable.fill.__name__))


class _Converter(_Matchable):

    def __init__(self, delegate, valFunc):
        self.delegate = delegate
        self.valFunc = valFunc

    def check(*args):
        # print("___", args)
        pass

    def fill(self, string, matchObject):
        # print(">>>", self, string, matchObject)
        return self.valFunc(self.delegate.fill(string, matchObject))


class _Group(_Matchable):
    def __init__(self, index):
        assert index >= 0, "Group requires non-negative index argument (got {})".format(index)
        self._index = index

        self.asInt = _Converter(self, int)

    def check(self, pattern):
        assert pattern.groups >= self._index, "Pattern {} has {} group(s) (got group index {})".format(pattern,
                                                                                                     pattern.groups,
                                                                                                     self._index)

    def fill(self, string, matchObject):
        # print("filling:", string, matchObject.groups())
        return matchObject.group(self._index)


def g(x: int):
    return _Group(x)


g0 = _Group(0)
g1 = _Group(1)
g2 = _Group(2)
g3 = _Group(3)
g4 = _Group(4)
g5 = _Group(5)
g6 = _Group(6)
g7 = _Group(7)
g8 = _Group(8)
g9 = _Group(9)
