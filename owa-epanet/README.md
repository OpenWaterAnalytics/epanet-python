# epanet python package

A slender, auto-generated python wrapper around owa:epanet hydraulic network analysis toolkit. This package uses SWIG and scikit-build to generate python bindings into the C library. The goal of this package is to establish basic python support for the toolkit, rather than present a "pythonic" interface. More abstractions can be built atop this package to further abstract the API, but the set of functions here is meant to (as closely as practical) mirror the well-known and established C API.

Where possible, SWIG has been configured to throw warnings/exceptions instead of using the customary EPANET return integer value for success-checking. Also any output (pointer) parameters from the C API have been re-routed to return values. In these cases, the return tuple from the Python API will contain the values desired.

```

./scripts/clean.sh
python3 setup.py sdist bdist_wheel
cd test && pipenv install ../dist/*.whl && pipenv run python -c 'from epanet import toolkit; print(toolkit.__dict__)'

```

This python library was packaged in the following way:

```
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
```
