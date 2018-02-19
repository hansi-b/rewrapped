TODO
====

#. None-match wrapping
#. more utility modders like split, join, etc.
#. what about more interesting regular expressions
  #. add support for named groups
  #. prevent confusion for groups from alternatives like "(ab)|(cd)"
#. is there a way to make use of `methods of the MatchObject interface <https://docs.python.org/3.6/library/re.html#match-objects>`_ ?
#. better exception handling: currently, we throw AssertionErrors



class _NoneMatch(object):
    """
        end
        endpos
        expand
        group
        groupdict
        groups
        lastgroup
        lastindex
        pos
        re
        regs
        span
        start
        string
    """
    
    def group(self, *_idx):return None

    def groups(self):return tuple()

    def groupDict(self):return dict()
