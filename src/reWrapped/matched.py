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
from reWrapped.modders import SingleValueField, TupleValueField


class _Group(SingleValueField):

    def __init__(self, index, defaultValue=None):
        super(_Group, self).__init__()
        assert index >= 0, "Group requires non-negative index argument (got {})".format(index)
        self._index = index
        self._defVal = defaultValue

    def check(self, pattern):
        assert pattern.groups >= self._index, \
            "Pattern {} has {} group(s) (got group index {})".format(pattern,
                                                                     pattern.groups,
                                                                     self._index)

    def fill(self, _string, matchObject):
        v = matchObject.group(self._index)
        return v if v is not None else self._defVal

    def __eq__(self, other):
        if not isinstance(other, _Group): return False
        return self._index == other._index and self._defVal == other._defVal
    
    def __hash__(self):
        return hash((self._index, self._defVal))

        
def g(idx: int):
    return _Group(idx)


def gOr(idx: int, defaultValue):
    return _Group(idx, defaultValue)


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


class _After(SingleValueField):

    def __init__(self):
        super(_After, self).__init__()
        
    def check(self, pattern):
        pass
    
    def fill(self, string, matchObject):
        return string[matchObject.end():]


class _Before(SingleValueField):
    
    def __init__(self):
        super(_Before, self).__init__()

    def check(self, pattern):
        pass
    
    def fill(self, string, matchObject):
        return string[:matchObject.start()]


after = _After()
before = _Before()

        
class _GroupTuple(TupleValueField):

    def __init__(self, *indices):
        super(_GroupTuple, self).__init__()
        assert len(indices) == 0 or min(indices) >= 0, \
            "GroupTuple requires non-negative index argument (got {})".format(indices)

        self._indices = tuple(indices)

    def check(self, pattern):
        if len(self._indices) > 0:
            assert pattern.groups >= max(self._indices), \
                "Pattern {} has {} group(s) (got group indices {})".format(pattern,
                                                                           pattern.groups,
                                                                           self._indices)
        else:
            assert pattern.groups > 1, \
                "Pattern {} has {} group(s) (got empty group indices)".format(pattern,
                                                                              pattern.groups,
                                                                              self._indices)

    def fill(self, _string, matchObject):
        if len(self._indices) == 0: return matchObject.groups()
        return tuple(matchObject.group(i) for i in self._indices)


def gTuple(*indices):
    return _GroupTuple(*indices)
