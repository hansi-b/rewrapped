# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
Provides modifiers for :class:`match fields <rewrapped.patterns.MatchField>` such as type conversions
and function applications.
"""

__author__ = "Hans Bering"
__copyright__ = "Copyright 2018"
__credits__ = ["Hans Bering"]
__license__ = "MIT License"
__maintainer__ = "Hans Bering"
__email__ = "hansi.b.github@moc.liamg"
__status__ = "Development"

from enum import Enum
from rewrapped.patterns import MatchField


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
    

class _BreakingModder(_Modder):

    def __init__(self, breakVal=None):
        self.breakVal = breakVal
    
    # FIXME this inheritance breaks with the modder contract
    def modit(self, val):
        status = _ModStatus.GoOn if val != self.breakVal else _ModStatus.Break 
        return val, status


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
        self._origin.check(pattern)

    
class SingleValueField(_ModdableField):
 
    def __init__(self, originField, modders=None):
        super(SingleValueField, self).__init__(originField, modders)
     
    _asInt = _Modder(int)
    _asFloat = _Modder(float)
    _strip = _Modder(lambda s:s.strip())

    @property
    def asInt(self):
        """
            Return the field value as an integer:
            
                >>> from rewrapped import ReWrap, matched
                >>> class Inventory(ReWrap):
                ...     matchOn = "([0-9]+)"
                ...     count = matched.g1.asInt
                ...
                >>> i = Inventory.search("there are 45 oranges left")
                >>> i.count
                45
                >>> type(i.count)
                <class 'int'>

        """
        return self._build(SingleValueField._asInt)

    @property
    def asFloat(self):
        """
            Return the field value as a float:
            
                >>> from rewrapped import ReWrap, matched
                >>> class Direction(ReWrap):
                ...     matchOn = "([0-9]+\.[0-9]+)"
                ...     distance = matched.g1.asFloat
                ...
                >>> d = Direction.search("left 3.12 km")
                >>> d.distance
                3.12
                >>> type(d.distance)
                <class 'float'>

        """
        return self._build(SingleValueField._asFloat)

    @property
    def strip(self):
        """
            Strip whitespace from the field value:
            
                >>> from rewrapped import ReWrap, matched
                >>> class FirstWord(ReWrap):
                ...     matchOn = "\s*\S+"
                ...     word = matched.g0.strip
                ...
                >>> f = FirstWord.search("  Make sweet some vial")
                >>> f.word
                'Make'

        """
        return self._build(SingleValueField._strip)

    def breakOn(self, breakVal=None):
        """
            Do not evaluate following field modifiers if the field value is the argument value;
            return that value instead:
            
                >>> from rewrapped import ReWrap, matched
                >>> class Quantity(ReWrap):
                ...     matchOn = "(NA|[0-9]+)"
                ...     amount = matched.g0.breakOn("NA").asInt
                ...
                >>> qs = Quantity.findall("measured NA 123")
                >>> tuple((q.amount, type(q.amount)) for q in qs)
                (('NA', <class 'str'>), (123, <class 'int'>))

        """
        return self._build(_BreakingModder(breakVal))

    @property
    def breakOnNone(self):
        """
            Do not evaluate following field modifiers if the field value is ``None``;
            return ``None`` as the value instead:
            
                >>> from rewrapped import ReWrap, matched
                >>> class Counted(ReWrap):
                ...     matchOn = "the ([0-9]+)?\s*parrots"
                ...     number = matched.g1.breakOnNone.asInt
                ...
                >>> c = Counted.search("the 24 parrots")
                >>> c.number
                24
                >>> c = Counted.search("the parrots")
                >>> c.number is None
                True

            Short for :func:`breakOn(None) <breakOn>`
        """
        return self.breakOn()

    def apply(self, valFunc):
        """
            Apply the argument function on the field value.
            
                >>> from rewrapped import ReWrap, matched
                >>> class Code(ReWrap):
                ...     matchOn = "letters: ([a-z ]+)"
                ...     letters = matched.g1.apply(set).apply(sorted)
                ...
                >>> c = Code.search("letters: a b a za b")
                >>> c.letters
                [' ', 'a', 'b', 'z']
        """
        return self._build(_Modder(valFunc))

    def _build(self, modder):
        return SingleValueField(self._origin, self._modders + (modder,))


class _MappingModder(_Modder):

    def __init__(self, singleValFunc):

        def mapMod(valTuple):
            return tuple(singleValFunc(v) for v in valTuple)

        super(_MappingModder, self).__init__(mapMod)


class TupleValueField(_ModdableField):
 
    def __init__(self, originField, modders=None):
        super(TupleValueField, self).__init__(originField, modders)

    _asInts = _MappingModder(int)
    _asFloats = _MappingModder(float) 

    @property
    def asInts(self):
        """
            Return the field values as integers:

                >>> from rewrapped import ReWrap, matched
                >>> class Inventory(ReWrap):
                ...     matchOn = "between ([0-9]+) and ([0-9]+)"
                ...     estimate = matched.gTuple(1,2).asInts
                ...
                >>> i = Inventory.search("there are between 45 and 67 oranges left")
                >>> i.estimate
                (45, 67)

        """
        return self._build(TupleValueField._asInts)

    @property
    def asFloats(self):
        """
            Return the field values as floats:

                >>> from rewrapped import ReWrap, matched
                >>> class ErrorMargin(ReWrap):
                ...     matchOn = "between ([0-9]+\.[0-9]+) and ([0-9]+\.[0-9]+)"
                ...     interval = matched.gTuple(1,2).asFloats
                ...
                >>> e = ErrorMargin.search("between 4.5 and 6.7 units")
                >>> e.interval
                (4.5, 6.7)
        """
        return self._build(TupleValueField._asFloats)
    
    def apply(self, valsFunc):
        """
            Apply the argument function on the field values. The function
            will be passed as many value arguments as the field has
            groups, in the field's order:
            
                >>> import datetime
                >>> from rewrapped import ReWrap, matched
                >>> class StartedDate(ReWrap):
                ...     matchOn = "started ([0-9]{4})-([0-9]{2})-([0-9]{2})"
                ...     when = matched.gTuple().asInts.apply(datetime.datetime)
                ...
                >>> s = StartedDate.search("started 1969-10-05")
                >>> s.when
                datetime.datetime(1969, 10, 5, 0, 0)
            
        """
        return self._build(_Modder(lambda vals, fn=valsFunc: fn(*vals))) 

    def _build(self, modder):
        return TupleValueField(self._origin, self._modders + (modder,))

