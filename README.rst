reWrapped
=========

reWrapped lets you write your regular expressions in a class-like
syntax with match groups flexibly mapped to named fields.

Example::

    from reWrapped import ReWrap, matched
    class NumericId(ReWrap):
         matchOn = "id ([0-9])+"
         idNo = matched.g1.asInt
