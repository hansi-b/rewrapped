# -*- coding: utf-8 -*-
# !/usr/bin/env python3

__author__ = "Hans Bering"
__copyright__ = "Copyright 2018"
__credits__ = ["Hans Bering"]
__license__ = "MIT License"
__maintainer__ = "Hans Bering"
__email__ = "hansi.b.github@moc.liamg"
__status__ = "Development"


import os
from setuptools import setup


# Utility function to read the README file.  
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="rewrapped",
    author="Hans Bering",
    author_email="hansi.b.github@moc.liamg",
    description=("Class wrappers for regular expressions "
                 "with proper fields for match groups."),
    license="MIT",
    url="https://github.com/hansi-b/rewrapped",
    package_dir={'':'src'},
    packages=("rewrapped",),
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
        "Topic :: Text Processing :: General",
        "Topic :: Utilities",
    ],

    use_scm_version=True,
    python_requires='>=3',
    setup_requires=[
        "setuptools_scm"
    ],
)
