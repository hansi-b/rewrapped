TODO
====

* better exception handling: currently, we throw AssertionErrors
* more utility methods like split, findall, etc.
* more flexible typing, e.g., asInts with convert::

    started = matched.gTuple().asInts.convert(lambda y, m, d:datetime.datetime(y, m, d))
