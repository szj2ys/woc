#!/bin/bash



# Use the Python executable provided from the `-p` option, or a default.
[ "$1" = "-p" ] && PYTHON=$2 || PYTHON="python3"

PACKAGE=$(basename `pwd`)

autoflake --recursive ${PACKAGE}
yapf -irp .
pip install -y ${PACKAGE}
python3 setup.py install



