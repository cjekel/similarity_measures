#!/usr/bin/env bash
rm -r docs
mkdir docs
pdoc --html -f --output-dir .docs_test similaritymeasures
cp -r .docs_test/similaritymeasures/* docs/
