#/bin/bash

# deactivate python virtual environment
#deactivate

# project root abs path
#PROJECT_DIR=$(dirname $(cd $(dirname "${BASH_SOURCE[0]}") && pwd))
PROJECT_DIR=`pwd`

ENVNAME=$(basename $PROJECT_DIR)

# remove kernel
jupyter kernelspec remove ${ENVNAME}

# remove pipenv from environment
pipenv --rm

# look over existing kernels
#${PREFIX}jupyter kernelspec list
