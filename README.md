# epanet-python
The home for Python packages related to the EPANET engine.


## Contents
* owa-epanet - the thinnest of SWIG-generated wrappers for EPANET. Updated frequently alongside OWA:EPANET.
* epanet-module - A ctypes based wrapper for the EPANET Toolkit (with support for reading EPANET binary output files).
* epanet-python - SWIG based wrappers for the EPANET Toolkit and Output libraries. Deprecated.


## Motivation
These Python wrappers for EPANET are available to developers interested in building higher level functionality on top.

## Which wrapper to use
This depends on user preference. Using a ctypes may have certain advantages. Alternatively, starting with an auto-generated python API wrapper is a good foundation for building more abstractions, and SWIG-wrapping means that the Python package gets automatically updated whenever new core features are available.

## Contributing
There are many ways for those interested in contributing to participate - providing software development support, helping with documentation, finding bugs, or contributing feature requests. Feel free to get involved! Just open an issue or chat with others on the [community forum](http://community.wateranalytics.org).
