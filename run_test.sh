#!/usr/bin/env bash
set -e 

#. ~/.virtualenvs/testproject/bin/activate
. /var/lib/jenkins/.virtualenvs/testproject/bin/activate

PYTHONPATH=. py.test
