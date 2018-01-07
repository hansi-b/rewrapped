TODO
====

#. more utility methods like split, findall, etc.
#. `methods of the MatchObject interface <https://docs.python.org/3.6/library/re.html#match-objects>`_
#. more flexible typing, e.g., asInts with convert::

    started = matched.gTuple().asInts.convert(lambda y, m, d:datetime.datetime(y, m, d))
    * add trim for string matches
#. better exception handling: currently, we throw AssertionErrors
