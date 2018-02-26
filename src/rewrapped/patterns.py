# -*- coding: utf-8 -*-
# !/usr/bin/env python3
"""
Provides the main :class:`~rewrapped.patterns.ReWrap` base class.
"""

__author__ = "Hans Bering"
__copyright__ = "Copyright 2017"
__credits__ = ["Hans Bering"]
__license__ = "MIT License"
__maintainer__ = "Hans Bering"
__email__ = "hansi.b.github@mgail.moc"
__status__ = "Development"

import re


class MatchField:
    """
    The marker class for which fields in :class:`~rewrapped.patterns.ReWrap` classes are initialized.
    Only defines the required behaviour: being able to check and fill a field.
    
    See :class:`~rewrapped.matched` for predefined fields.
    """

    def check(self, pattern):
        """
        Does an optional static check of this field against the argument ``Pattern`` object,
        if applicable.
        
        :return: nothing; raise an Error on failure
        """
        raise NotImplementedError("{} requires method '{}'".format(self.__class__.__name__,
                                                                   MatchField.check.__name__))

    def fill(self, string, matchObject):
        """
        Evaluate this field with regard to a match object that was found in the argument string.
        
        :return: this field's value (e.g., a match object group or groups)
        """
        raise NotImplementedError("{} requires method '{}'".format(self.__class__.__name__,
                                                                   MatchField.fill.__name__))


class _MetaReClass(type):
    """
        The minimal factory class for ``ReWrap`` classes.
        * Augments each ReWrap with that class's compiled pattern,
        * lets the class fields check themselves against the pattern, and
        * collects the fields for filling on instantiation.
    """
    
    def __init__(cls, name, _bases, clsDict):
        assert "matchOn" in clsDict, "ReWrap {} requires field 'matchOn'".format(name)

        pattern = _MetaReClass.__compile(cls.matchOn)
        setattr(cls, "_pattern", pattern)
        setattr(cls, "_fields", _MetaReClass._get_fields(cls, clsDict, pattern))

    @staticmethod
    def __compile(matchOn):
        if matchOn is None: return None
        if isinstance(matchOn, tuple):
            assert len(matchOn) == 2, "Invalid tuple argument %s of len %d (require len 2)".format(matchOn, len(matchOn))
            return re.compile(*matchOn)
        return re.compile(matchOn)

    @staticmethod
    def _get_fields(cls, clsDict, pattern):
        fields = []
        for name, element in clsDict.items():
            if isinstance(element, MatchField):
                element.check(pattern)
                fields.append((name, element))

        return tuple(fields)


class _NoneMatch:

    def group(self, *_args):
        return None

    def end(self):
        return None

    def start(self):
        return None


class ReWrap(metaclass=_MetaReClass):
    """
    The base class from which to inherit your own pattern definition.
    
    Every such class must have a :attr:`~rewrapped.patterns.ReWrap.matchOn` field (usually a string or
    `pattern object <https://docs.python.org/3/library/re.html#regular-expression-objects>`_) 
    defining what instances of the class are to match.
    
    In order to be useful, the class also has to contain
    :mod:`match fields <rewrapped.matched>` to refer to match contents.
    
    """
    _pattern = None
    _fields = None

    matchOn = None
    """
    The pattern on which this class should match. Every ``ReWrap`` subclass
    has to define this field. It can be anything that can passed to
    `re.compile <https://docs.python.org/3/library/re.html#re.compile>`_, e.g.:
            
    >>> from rewrapped import ReWrap
    >>> class Word(ReWrap):
    ...     matchOn = "\w+"
    ...     
    >>> 

    If the argument is a string, is is compiled to a pattern object at class compile time,
    so any error is detected at that point:
    
    >>> from rewrapped import ReWrap
    >>> class Word(ReWrap):
    ...     matchOn = "(\w+]"
    ... 
    Traceback (most recent call last):
     ...
    sre_constants.error: missing ), unterminated subpattern at position 0


    The string can optionally be followed by match flags
    in the manner one would pass them to ``re.compile``:

    >>> from re import IGNORECASE, MULTILINE    
    >>> from rewrapped import ReWrap,matched
    >>> class Word(ReWrap):
    ...     matchOn = "^abc", IGNORECASE | MULTILINE
    ...     abc = matched.g0
    ...     
    >>> m = Word.search("123\\nABC")
    >>> m.abc
    'ABC'

    """
    
    wrapNone = False
    """
    A boolean flag indicating whether to wrap a ``None`` no-match result in an instance of the respective ``ReWrap`` subclass.
    All groups of that instance will evaluate to ``None``, and :data:`~rewrapped.matched.before` and
    :data:`~rewrapped.matched.after` match fields will both yield the
    complete searched (and unmatched) string.

    >>> from rewrapped import ReWrap,matched
    >>> class Word(ReWrap):
    ...     matchOn = "abc"
    ...     wrapNone = True
    ...     abc = matched.g0
    ...     before = matched.before
    ...     after = matched.after
    ...     
    >>> m = Word.search("nothing here")
    >>> type(m)
    <class 'Word'>
    >>> m.abc is None
    True
    >>> m.before
    'nothing here'
    >>> m.after
    'nothing here'


    Only affects methods which can return ``None`` results (e.g., :func:`~rewrapped.patterns.ReWrap.search`);
    does not affect methods which return collections or iterators (e.g., :func:`~rewrapped.patterns.ReWrap.findall`).
    
    Defaults to ``False``: Return ``None`` when no match has been found.
    
    You *can* set this on the ``ReWrap`` baseclass directly if you want it to apply to *all* your
    subclasses.

    """

    def __init__(self, string, mObj):
        """
        Should not be called directly, but is done through the class
        methods.

        Fills an instance of this class with the match information of
        having matched against the argument string.
        
        :param string: the string against which this instance matched
        :param mObj: the resulting not-``None`` match object
        """
        assert mObj
        for name, field in self._fields:
            setattr(self, name, field.fill(string, mObj))
        
    def __repr__(self):
        valsStrings = []
        for fieldName, _f in self._fields:
            rawVal = getattr(self, fieldName, None)
            strVal = '"{}"'.format(rawVal) if isinstance(rawVal, str) else rawVal
            valsStrings.append("{}={}".format(fieldName, strVal))
            
        return "{}({})".format(self.__class__.__name__, ", ".join(valsStrings))

    @classmethod
    def _delegate(cls, pFunc, string, *args, **kwargs):
        """
            delegate and perhaps init a result
        """
        mObj = pFunc(string, *args, **kwargs)
        if mObj is None and cls.wrapNone:
            mObj = _NoneMatch()
        return cls(string, mObj) if mObj else None

    @classmethod
    def search(cls, string, *args, **kwargs):
        """
        A wrapper for ``re.regex.search``: Searches for a match in the argument string.
        Takes optional parameters like ``re.regex.search``.     
        :param string: the string in which to search
        :return: an instance of this class, if a match was found; ``None`` otherwise
    
        :see: https://docs.python.org/3.6/library/re.html#re.regex.search
        """
        return cls._delegate(cls._pattern.search, string, *args, **kwargs)

    @classmethod
    def match(cls, string, *args, **kwargs):
        """
        A wrapper for ``re.regex.match``: Tries to match the argument string from the beginning.
        Takes optional parameters like ``re.regex.match``.
        
        :param string: the string which to match from the beginning
        :return: an instance of this class, if a match was found; ``None`` otherwise
    
        :see: https://docs.python.org/3.6/library/re.html#re.regex.match
        """
        return cls._delegate(cls._pattern.match, string, *args, **kwargs)

    @classmethod
    def fullmatch(cls, string, *args, **kwargs):
        """
        A wrapper for ``re.regex.fullmatch``: Tries to match the argument string completely.
        Takes optional parameters like ``re.regex.fullmatch``.
        
        :param string: the string which to match
        :return: an instance of this class, if the string is a match; ``None`` otherwise
    
        :see: https://docs.python.org/3.6/library/re.html#re.regex.fullmatch
        """
        return cls._delegate(cls._pattern.fullmatch, string, *args, **kwargs)

    @classmethod
    def finditer(cls, string, *args, **kwargs):
        """
        A wrapper for ``re.regex.finditer``: Returns an iterator over non-overlapping matches
        in the argument string. Takes optional parameters like ``re.regex.finditer``.
        
        :param string: the string in which to search
        :return: an iterator, possibly empty, over instances of this class

        :see: https://docs.python.org/3.6/library/re.html#re.regex.finditer
        
        """
        return (cls(string, mObj) for mObj in cls._pattern.finditer(string, *args, **kwargs))

    @classmethod
    def findall(cls, string, *args, **kwargs):
        """
        A wrapper for ``re.regex.findall``; just wraps a list around this class's finditer
        
        :param string: the string in which to search
        :return: a list of all match instances on the argument string
        
        :see: https://docs.python.org/3.6/library/re.html#re.regex.findall
        """
        return list(cls.finditer(string, *args, **kwargs))

