#!/usr/bin/env bash

rm -rf \
packages/epanet/toolkit.py \
packages/epanet/output.py \
packages/epanet/*.so \
packages/epanet/*.dylib \
_skbuild \
_cmake_test_compile \
dist \
packages/epanet.egg-info \
test/*

touch test/Pipfile
