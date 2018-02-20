rewrapped
=========

.. image:: https://travis-ci.org/hansi-b/rewrapped.svg?branch=master
    :target: https://travis-ci.org/hansi-b/rewrapped
.. image:: https://codecov.io/gh/hansi-b/rewrapped/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/hansi-b/rewrapped
    
For the time being, more documentation is at
`this project's github pages <https://hansi-b.github.io/rewrapped/>`_.

rewrapped lets you write your regular expressions as classes
with match groups flexibly mapped to named fields.

A simple example:

.. code:: python

    from rewrapped import ReWrap, matched
    class Inventory(ReWrap):
        matchOn = "([0-9]+)\s+(\S+)"
        count = matched.g1.asInt
        item = matched.g2

This will yield match results which map the first match field
to the integer ``count``, and the second to the string field ``item``:

.. code:: python

      >>> i = Inventory.search("there are 45 oranges left")
      >>> i.count
      45
      >>> i.item
      'oranges'
      >>> 
