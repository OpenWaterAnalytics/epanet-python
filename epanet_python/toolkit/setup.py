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
#


from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


setup(
    name = 'epanet.toolkit',
    version = "0.0.3a0",
    ext_modules = [
        Extension("epanet.toolkit._toolkit",
            sources = ['epanet/toolkit/toolkit_wrap.c'],
            include_dirs = ['epanet/toolkit'],
            library_dirs = ['epanet/toolkit'],
            libraries = ['epanet_py'],
            language = 'C'
        )
    ],

    # tox can't find epanet module at test time unless namespace is declared
    namespace_packages = ['epanet'],

    packages = {'epanet.toolkit'},
    py_modules = ['toolkit'],
    package_data = {'epanet.toolkit':['*epanet_py.dll', '*epanet_py.so']},

    zip_safe=False

)
