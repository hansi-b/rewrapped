rewrapped
=========

.. image:: https://travis-ci.org/hansi-b/rewrapped.svg?branch=master
    :target: https://travis-ci.org/hansi-b/rewrapped

.. image:: https://codecov.io/gh/hansi-b/rewrapped/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/hansi-b/rewrapped

.. image:: https://badge.fury.io/py/rewrapped.svg
   :target: https://badge.fury.io/py/rewrapped

rewrapped is an exercise in Python metaclass usage. It allows you to wrap your regular expression in a Python class along with named and
typed fields for match groups. The classes provide static search functionality mostly identical to the ``re`` module, and
match results are flexibly mapped to named instance fields of the proper type.

To do so,

#. subclass from ``rewrapped.patterns.ReWrap``,
#. put the regular expression in the special ``matchOn`` class field, and
#. add match class fields to refer to match results.

A simple example:

.. code:: python

    from rewrapped import ReWrap, matched

    # ReWrap is the required base class
    class Inventory(ReWrap):

        # matchOn is the fixed
        # regular expression class field
        matchOn = "([0-9]+)\s+(\S+)"

        # the matched module contains transformations
        # for match groups
        count = matched.g1.asInt
        item = matched.g2

This defines a class that would map the first match group of a match result
to the integer ``count``, and the second to the string field ``item``.
You use it like you would call, e.g., ``re.search``:

.. code:: python

      >>> i = Inventory.search("there are 45 oranges left")
      >>> i.count
      45
      >>> i.item
      'oranges'
      >>> 

The whole documentation including examples is at
`this project's github pages <https://hansi-b.github.io/rewrapped/>`_.
