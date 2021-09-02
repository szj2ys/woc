#/bin/bash

# deactivate python virtual environment
deactivate

# get the pypi source, default pypi, and aliyun is an option
read -p "请输入Python源[pypi:default, aliyun]: " SOURCE


# project root abs path
#PROJECT_DIR=$(dirname $(cd $(dirname "${BASH_SOURCE[0]}") && pwd))
PROJECT_DIR=`pwd`

# pipenv path
PIPENV=`pipenv --venv`
PREFIX="${PIPENV}/bin/"
PIP="${PIPENV}/bin/pip"

# requirments file
read -p "请输入requirements文件名: " input
if [ ! -n "$input" ] ;then
    REQUIREMENTS_FILE='requirements.txt'
else
    REQUIREMENTS_FILE=${input}
fi

# install requirements.txt packages
echo "installing python package ..."
${PIP} install --upgrade pip
while read PKG
do
  if [ "${SOURCE}" = "pypi" ]; then
    ${PIP} install ${PKG} -i https://pypi.org/simple
  elif [ "${SOURCE}" = "aliyun" ]; then
    ${PIP} install ${PKG} -i https://mirrors.aliyun.com/pypi/simple
  else
    ${PIP} install ${PKG} -i https://pypi.org/simple
  fi
done  < ${PROJECT_DIR}/${REQUIREMENTS_FILE}
