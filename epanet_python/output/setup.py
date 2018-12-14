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
    name = microlib_name,
    version = "0.1.2a0",
    ext_modules = [
        Extension("epanet.output._output",
            include_dirs = ['epanet/output'],
            libraries = ['epanet-output'],
            library_dirs = ['epanet/output'],
            sources = ['epanet/output/output.i'],
            swig_opts=['-py3'],
            language = 'C'
        )
    ],
    namespace_packages=['epanet'],
    packages = {microlib_name},
#    py_modules = ['output'],
#    include_package_data=True
    package_data = {microlib_name:['*epanet-output.dll', '*epanet-output.so']},

#    install_requires = []
)
