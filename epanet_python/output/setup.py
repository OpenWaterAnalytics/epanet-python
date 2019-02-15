# -*- coding: utf-8 -*-
#
# setup.py
#
# Created:    9/20/2017
# Author:     Michael E. Tryby
#             US EPA - ORD/NRMRL
#
# Setup up script for en_outputapi python extension
#
# Requires:
#   Platform C language compiler
#   Python packages: numpy
#

try:
    from setuptools import setup, Extension
    from setuptools.command.build_ext import build_ext
except ImportError:
    from distutils.core import setup, Extension
    from distutils.command.build_ext import build_ext


microlib_name = 'epanet.output'

setup(
    name = 'epanet.output',
    version = "0.1.2a0",
    ext_modules = [
        Extension("epanet.output._output",
            sources = ['epanet/output/output_wrap.c'],
            include_dirs = ['epanet/output'],
            libraries = ['epanet-output'],
            library_dirs = ['epanet/output'],
            language = 'C'
        )
    ],

    # tox can't find swmm module at test time unless namespace is declared
    namespace_packages=['epanet'],

    packages = {'epanet.output'},
    py_modules = ['output'],
    package_data = {'epanet.output':['*epanet-output.dll', '*epanet-output.so']},

    zip_safe=False,
)
