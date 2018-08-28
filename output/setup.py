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

setup(
    name = "epanet_output", 
    version = "0.1.1-alpha",
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
    packages = {'epanet.output'},  
    py_modules = ['output'],
    package_data = {'epanet.output':['*epanet-output.dll', '*epanet-output.so']}, 
 
    install_requires = [
        'aenum'
    ]
)
