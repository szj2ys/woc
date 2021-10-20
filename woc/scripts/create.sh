#/bin/bash


# deactivate python virtual environment
#deactivate

# project root abs path
PROJECT_DIR=`pwd`

ENVNAME=$(basename $PROJECT_DIR)
echo "Virtual environment [01;31m$ENVNAME[0m will be create"

read -r -p "Are You Sure? [Y/n] " input

case $input in
    [yY][eE][sS]|[yY])
    echo "Yes"
    ;;

    [nN][oO]|[nN])
    echo "No"
    exit 1
    ;;

    *)
    echo "Invalid input..."
    exit 1
    ;;
esac

# create virtual environment, use default python version
pipenv --python `which python3`
#read -p "请输入Python版本: " input
#if [ ! -n "$input" ] ;then
#    pipenv --python `which python3`
#else
#    pipenv --python ${input}
#fi

PIPENV=`pipenv --venv`
PREFIX="${PIPENV}/bin/"
PIP="${PIPENV}/bin/pip"

# 将环境配置到jupyter notebook中
read -r -p "将环境配置到jupyter notebook中? [Y/n] " input

case $input in
    [yY][eE][sS]|[yY])
    python3 -m ipykernel install --user --name=${ENVNAME}
    ;;

    [nN][oO]|[nN])
    echo "No"
    ;;

    *)
    echo "No"
    ;;
esac

## look over existing kernels
#${PREFIX}jupyter kernelspec list

