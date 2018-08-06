# -*- coding: utf-8 -*-
#
# setup.py - Setup up script for en_toolkit python extension
# 
# Created:    11/27/2017
# Author:     Michael E. Tryby
#             US EPA - ORD/NRMRL
#
# Requires:
#   Platform C language compiler   
#   SWIG
#

try:
    from setuptools import setup, Extension
    from setuptools.command.build_ext import build_ext
except ImportError:
    from distutils.core import setup, Extension
    from distutils.command.build_ext import build_ext

setup(
    name = "epanet_toolkit", 
    version = "0.0.1",
    ext_modules = [
        Extension("epanet.toolkit._toolkit",
            include_dirs = ['epanet/toolkit/'],
            libraries = ['epanet'],
            library_dirs = ['epanet/toolkit'],
            sources = ['epanet/toolkit/toolkit.i'],
            swig_opts=['-py3'],
            language = 'C'
        )
    ],
    packages = {'epanet.toolkit'},  
    py_modules = ['toolkit'],
    package_data = {'epanet.toolkit':['*epanet.dll', '*epanet.so']}, 
      
    install_requires = [
        'enum34'
    ]
)
