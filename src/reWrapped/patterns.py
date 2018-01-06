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

from reWrapped import matched


class _MetaReClass(type):
    """
        The minimal factory class for ``ReWrap`` classes.
        * Augments each ReWrap with that class's compiled pattern,
        * lets the class fields check themselves against the pattern, and
        * collects the fields for filling on instantiation.
    """

    def __init__(cls, name, _bases, clsDict):
        assert "matchOn" in clsDict, "ReWrap {} requires field 'matchOn'".format(name)

        pattern = re.compile(cls.matchOn) if cls.matchOn is not None else None
        setattr(cls, "_pattern", pattern)
        setattr(cls, "_fields", _MetaReClass._get_fields(cls, clsDict, pattern))

    @staticmethod
    def _get_fields(cls, clsDict, pattern):
        fields = set()
        for name, element in clsDict.items():
            if isinstance(element, matched.MatchField):
                element.check(pattern)
                fields.add((name, element))

        return fields


class ReWrap(metaclass=_MetaReClass):
    """
    The base class from which to inherit your own pattern definition.
    
    Every such class must have a ``matchOn`` field (usually a string or
    Pattern instance) defining the expression instances of the class
    are to match.

    """
    _pattern = None
    _fields = None

    matchOn = None

    def __init__(self, string, mObj):
        """
            Should not be called directly, but is done through the class
            methods.

            Fills an instance of this class with the match information of
            having matched against the argument string.
            
            :param string: the string against which this instance matched
            :param mObj: the resulting not-None match object
        """
        assert mObj
        for name, field in self._fields:
            setattr(self, name, field.fill(string, mObj))

    @classmethod
    def _delegate(cls, pFunc, string, *args, **kwargs):
        """
            delegate and perhaps init a result
        """
        mObj = pFunc(string, *args, **kwargs)
        return cls(string, mObj) if mObj else None

    @classmethod
    def search(cls, string, *args, **kwargs):
        """
        A wrapper for ``re.regex.search``: Searches for a match in the argument string.
        Takes optional parameters like ``re.regex.search``.     
        :param string: the string in which to search
        :return: an instance of this class, if a match was found; None otherwise
    
        :see: https://docs.python.org/3.6/library/re.html#re.regex.search
        """
        return cls._delegate(cls._pattern.search, string, *args, **kwargs)

    @classmethod
    def match(cls, string, *args, **kwargs):
        """
        A wrapper for ``re.regex.match``: Tries to match the argument string from the beginning.
        Takes optional parameters like ``re.regex.match``.
        
        :param string: the string which to match from the beginning
        :return: an instance of this class, if a match was found; None otherwise
    
        :see: https://docs.python.org/3.6/library/re.html#re.regex.match
        """
        return cls._delegate(cls._pattern.match, string, *args, **kwargs)

    @classmethod
    def fullmatch(cls, string, *args, **kwargs):
        """
        A wrapper for ``re.regex.fullmatch``: Tries to match the argument string completely.
        Takes optional parameters like ``re.regex.fullmatch``.
        
        :param string: the string which to match
        :return: an instance of this class, if the string is a match; None otherwise
    
        :see: https://docs.python.org/3.6/library/re.html#re.regex.fullmatch
        """
        return cls._delegate(cls._pattern.fullmatch, string, *args, **kwargs)


if __name__ == "__main__":
    pass
