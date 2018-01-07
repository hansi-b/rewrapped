reWrapped
=========

reWrapped lets you write your regular expressions in a class-like
syntax with match groups flexibly mapped to named fields.

A simple example::

    from reWrapped import ReWrap, matched
    class Inventory(ReWrap):
        matchOn = "([0-9]+)\s+(\S+)"
        count = matched.g1.asInt
        item = matched.g2

This will yield match results which map the first match field
to the integer ``count``, and the second to the string field ``item``::

      >>> i = Inventory.search("there are 45 oranges left")
      >>> i.count
      45
      >>> i.item
      'oranges'
      >>> 
