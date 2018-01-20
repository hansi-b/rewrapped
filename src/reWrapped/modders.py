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
from enum import Enum
from reWrapped.patterns import MatchField


class _ModStatus(Enum):
    GoOn = 0
    Break = 1


class _Modder:

    def __init__(self, valFunc):
        self.valFunc = valFunc

    def modit(self, val):
        """
            The default modder: applies its own value function
            :return: a pair (new value, status)
        """
        return self.valFunc(val), _ModStatus.GoOn


class _ModdableField(MatchField):
    
    def __init__(self, originField, modders=None):
        self._origin = originField
        self._modders = modders or tuple()

    def fill(self, string, matchObject):
        val = self._origin.fill(string, matchObject)
        for m in self._modders:
            val, status = m.modit(val)
            if status == _ModStatus.Break: break
        return val

    def check(self, pattern):
        pass

    def __eq__(self, other):
        if not isinstance(other, _ModdableField):
            return False
        
        return self._origin == other._origin and self._modders == other._modders

    def __hash__(self):
        return (self._origin, self._modders).__hash__()

    
class SingleValueField(_ModdableField):
 
    def __init__(self, originField=None, modders=None):
        super(SingleValueField, self).__init__(originField or self, modders)
     
    _asInt = _Modder(int)
    _asFloat = _Modder(float)    

    @property
    def asInt(self):
        return self._build(SingleValueField._asInt)

    @property
    def asFloat(self):
        return self._build(SingleValueField._asFloat)

    def convert(self, valFunc):
        return self._build(_Modder(valFunc)) 

    def _build(self, modder):
        print("_build SingleValueField: {}".format(self.__class__))
        return SingleValueField(self._origin, self._modders + (modder,))


class _MappingModder(_Modder):

    def __init__(self, singleValFunc):

        def mapMod(valTuple):
            return tuple(singleValFunc(v) for v in valTuple)

        super(_MappingModder, self).__init__(mapMod)


class TupleValueField(_ModdableField):
 
    def __init__(self, originField=None, modders=None):
        super(TupleValueField, self).__init__(originField or self, modders)

    _asInts = _MappingModder(int)
    _asFloats = _MappingModder(float) 

    @property
    def asInts(self):
        return self._build(TupleValueField._asInts)

    @property
    def asFloats(self):
        return self._build(TupleValueField._asFloats)
    
    def convert(self, valsFunc):
        return self._build(_Modder(lambda vals, fn=valsFunc: fn(*vals))) 

    def _build(self, modder):
        print("_build TupleValueField: {}".format(self.__class__))
        return TupleValueField(self._origin, self._modders + (modder,))


if __name__ == '__main__':
    pass
