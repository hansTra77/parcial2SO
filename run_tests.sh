#!/usr/bin/env bash
set -e 

. ~/.virtualenvs/testproject/bin/activate

PYTHONPATH=. py.test --junitxml=python_tests.xml
