.. src documentation master file, created by
   sphinx-quickstart on Sun Jan 21 13:19:48 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to reWrapped's documentation!
=====================================

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

.. toctree::
   :maxdepth: 4
   :caption: Contents:

   reWrapped


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
