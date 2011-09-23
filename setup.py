#!/usr/bin/env python
#
# Copyright (c) 2011 Vit Suchomel and Jan Pomikalek
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

from distutils.core import setup

setup(
    name='chared',
    version='1.2',
    description='Character encoding detection tool',
    long_description='''chared is a tool for detecting the character encoding
    of a text in a known language. The language of the text has to be
    specified as an input parameter so that correspondent language model
    can be used. The package contains models for a wide range of languages. In
    general, it should be more accurate than character encoding detection
    algorithms with no language constraints.''',
    author='Vit Suchomel and Jan Pomikalek',
    author_email='chared@sketchengine.co.uk',
    url='http://code.google.com/p/chared/',
    license='BSD',
    requires=['lxml (>=2.2.4)'],
    packages=['chared', 'chared.util'],
    package_data={'chared': ['models/*']},
    scripts=['bin/chared', 'bin/chared-learn'],
)
