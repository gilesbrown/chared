# Copyright (c) 2011 Vit Suchomel and Jan Pomikalek
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

try:
    __version__ = 'v' + __import__('pkg_resources').get_distribution('chared').version
except:
    __version__ = 'r$Rev$'
