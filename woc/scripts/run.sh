#/bin/bash

# get the python script
PYTHON_SCRIPTS=$1
DATETIME=`date +%Y-%m-%d:%H:%M:%S`

# project root abs path
#PROJECT_DIR=$(dirname $(cd $(dirname "${BASH_SOURCE[0]}") && pwd))
PROJECT_DIR=`pwd`

# temporary export project to environment
export PYTHONPATH=$PYTHONPATH:${PROJECT_DIR}

# pipenv path
PIPENV='/usr/local/bin/pipenv'

# log files dir
LOGS_DIR=${PROJECT_DIR}/logs
if [ ! -d $LOGS_DIR ]; then
    mkdir -p $LOGS_DIR
    echo "created logs directory: path=$LOGS_DIR"
fi
PYTHON_FILE=$(basename $PYTHON_SCRIPTS)
LOG_FILE=${LOGS_DIR}/${PYTHON_FILE%.*}${DATETIME}.log
ABS_PYTHON_SCRIPT=${PROJECT_DIR}/${PYTHON_SCRIPTS}

# translate time to readable
swap_seconds () {
        SEC=$1

        (( SEC < 60 )) && echo "[01;34m Execute elapsed time: ${PYTHON_FILE} seconds[0m"

        (( SEC >= 60 && SEC < 3600 )) && echo "[01;34m Execute ${PYTHON_FILE} elapsed time: $(( SEC / 60 )) min $(( SEC % 60 )) sec[0m"

        (( SEC > 3600 )) && echo "[01;34m Execute ${PYTHON_FILE} elapsed time: $(( SEC / 3600 )) hr $(( (SEC % 3600) / 60 )) min $(( (SEC % 3600) % 60 )) sec[0m"
}

start=$(date +%s)

# execute python script
${PIPENV} run python3 ${ABS_PYTHON_SCRIPT} >>${LOG_FILE} 2>&1 &

# wait task finished
wait

end=$(date +%s)

# show in terminal
while read str; do
    echo $str
done <${LOG_FILE}
swap_seconds $(( end - start ))

# remove out of date log file
find ${LOGS_DIR} -mtime +2 -name "*.log" -exec rm -rf {} \;

