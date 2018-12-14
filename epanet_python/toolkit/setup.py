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


microlib_name = 'epanet.toolkit'

setup(
    name = microlib_name,
    version = "0.0.2a0",
    ext_modules = [
        Extension("epanet.toolkit._toolkit",
            sources = ['epanet/toolkit/toolkit.i'],
            swig_opts = ['-py3'],
            include_dirs = ['epanet/toolkit'],
            library_dirs = ['epanet/toolkit'],
            libraries = ['epanet2'],
            extra_compile_args = ["/D WITH_GENX"],
            language = 'C'
        )
    ],
    namespace_packages = ['epanet'],
    packages = {microlib_name},
#    py_modules = ['toolkit'],
#    include_package_data=True
    package_data = {microlib_name:['*epanet2.dll', '*epanet2.so']},

)
