reWrapped
=========

For the time being, more documentation is at
`this project's github pages <https://hansi-b.github.io/reWrapped/>`_.

reWrapped lets you write your regular expressions in a class-like
syntax with match groups flexibly mapped to named fields without
having to resort to symbolic group names in your regular expressions
(unless you are doing really fancy stuff).

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
