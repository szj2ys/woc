#!/bin/sh -e


PACKAGE=$(basename `pwd`)

autoflake --recursive ${PACKAGE}
yapf -irp .
python3 setup.py sdist bdist_wheel --universal
twine upload dist/*
#${PREFIX}mkdocs gh-deploy --force

