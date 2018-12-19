# epanet-python
Is home for Python packages related to the EPANET engine. 

## Contents
* epanet-module - A ctypes based wrapper for the EPANET Toolkit (with support for reading EPANET binary output files).
* epanet-python - SWIG based wrappers for the EPANET Toolkit and Output libraries. 
* ...

## Motivation
These Python wrappers for EPANET are available to developers interested in building higher level functionality on top. Starting with a clean, auto-generated python API wrapper is a good foundation for building more abstractions. This also intersects with the near-term needs of the GUI work (which uses python and QT) - SWIG-wrapping will mean that the epanet library becomes scriptable from within the GUI.

Another benefit of auto-generating the wrapper is that it's fairly unambiguous; nobody's personal preferences get involved until we get to slightly higher-level abstractions, but everyone can share and benefit from the foundational SWIG layer.

## Contributing
There are many ways for those interested in contributing to participate - providing software development support, helping with documentation, finding bugs, or contributing feature requests. Feel free to get involved! 
