.. src documentation master file, created by
   sphinx-quickstart on Sun Jan 21 13:19:48 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to reWrapped's documentation!
=====================================

reWrapped lets you write your regular expressions as classes
with match groups flexibly mapped to named fields.

To do so,

#. subclass from :class:`~reWrapped.patterns.ReWrap`,
#. put the regular expression in the special ``matchOn`` class field, and
#. add :mod:`match fields <reWrapped.matched>` to refer to match results.

A simple example for a ``ReWrap`` class with two match fields::

    from reWrapped import ReWrap, matched
    class Inventory(ReWrap):
        matchOn = "([0-9]+)\s+(\S+)"
        count = matched.g1.asInt
        item = matched.g2

``ReWrap`` subclasses provide the usual bag of regular expression search methods
(:func:`search <reWrapped.patterns.ReWrap.search>`, :func:`match <reWrapped.patterns.ReWrap.match>`, etc.) as class methods,
and return instances of the respective class which evaluate the match fields from matched results.
E.g., the ``Inventory`` defined above would map the first match group
as an integer to the field ``count``, and the second to the string field ``item``:

  .. testsetup::

    from reWrapped import ReWrap, matched
    class Inventory(ReWrap):
        matchOn = "([0-9]+)\s+(\S+)"
        count = matched.g1.asInt
        item = matched.g2

  .. doctest::

   >>> i = Inventory.search("there are 45 oranges left")
   >>> type(i)
   <class 'Inventory'>
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

Kudos
=====
... go to https://daler.github.io/sphinxdoc-test/includeme.html and https://gist.github.com/brantfaircloth/791759
for their detailed accounts on how to get the sphinx documentation into the `gh-pages` branch!

Pulse
=====

.. image:: https://travis-ci.org/hansi-b/reWrapped.svg?branch=master
    :target: https://travis-ci.org/hansi-b/reWrapped
.. image:: https://codecov.io/gh/hansi-b/reWrapped/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/hansi-b/reWrapped
