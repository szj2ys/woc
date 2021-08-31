#!/bin/bash


PACKAGE=$(basename `pwd`)

if [ -d 'dist' ] ; then
    rm -rf dist
fi
if [ -d 'build' ] ; then
    rm -rf build
fi
if [ -d 'site' ] ; then
    rm -rf site
fi
if [ -d *.egg-info ] ; then
    rm -rf *.egg-info
fi

find ${PACKAGE} -type f -name "*.py[co]" -delete
find ${PACKAGE} -type d -name __pycache__ -delete
