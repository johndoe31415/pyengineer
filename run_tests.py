#!/bin/bash
#
#

if [ "$1" == "" ]; then
	python3 -m unittest pyengineer.tests
else
	python3 -m unittest "pyengineer.tests.${1}"
fi
