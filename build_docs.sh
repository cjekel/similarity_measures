#!/usr/bin/env bash
rm -r docs
mkdir docs
pdoc similaritymeasures -o docs -d numpy
