#!/bin/bash


PYTHON_FILE=$1   # Python脚本路径
DO=$3               # 获得要进行操作的指令
ALIAS=$2            # 数据库配置



# PYTHON_FILE的运行log日志
LOGS_DIR=logs
if [ ! -d $LOGS_DIR ]; then
    mkdir -p $LOGS_DIR
    echo "created logs directory: path=$LOGS_DIR"
fi
STDOUT_FILE=${LOGS_DIR}/${PYTHON_FILE%.*}.log

checkpid() {
    PSID=$(ps | grep $PYTHON_FILE| grep -v "grep" | grep -v "$0" | awk '{print $1}')
    echo '执行了'
    echo "ps | grep $PYTHON_FILE| grep -v "grep" | grep -v "$0"| awk '{print $1}'"
    # -n 如果字符串非空，则返回True
    if [ -n "$PSID" ]; then
       return $PSID   # 如果程序正在运行则返回 psid
    else
      return 0  # 如果程序未运行则返回 0
    fi
}

###################################
#(函数)启动程序
 #
 #说明：
 # 如果程序已经启动（$PSID不等于0），则提示程序已启动
 # 如果程序没有被启动，则执行启动命令行
 # 启动命令执行后，再次调用checkpid函数如果能够确认程序的PSID,则打印[OK]，否则打印[Failed]
 #注意：echo -n 表示打印字符后，不换行
 #注意: "nohup 某命令 >>/dev/null 2>&1 &" 的用法
###################################
start() {
   checkpid

   if [ "$?" -ne 0 ]; then
      echo "================================"
      echo "warn: $PYTHON_FILE already started! (psid=$PSID)"
      echo "================================"
   else
      echo "Starting $PYTHON_FILE ..."
#      echo "python3 ${PYTHON_FILE} --env=${ENV} --alias=${ALIAS} >&1 &"
      nohup python3 ${PYTHON_FILE} --alias=${ALIAS} >>${STDOUT_FILE} 2>&1 &
#      nohup python3 ${APP_HOME}/${PYTHON_FILE} >&1 &
      sleep 1

      checkpid
      if [ "$?" -ne 0 ]; then
         echo "[OK] (psid=$PSID)"
      else
         echo "[Failed]"
      fi
   fi
}

###################################
#(函数)检查程序运行状态
#
#说明：
#1. 首先调用checkpid函数
#2. 如果程序已经启动（$PSID不等于0），则提示正在运行并表示出PSID
#3. 否则，提示程序未运行
###################################
status() {
   checkpid
   if [ "$?" -ne 0 ]; then
      echo "$PYTHON_FILE is running! (psid=$PSID)"
   else
      echo "$PYTHON_FILE is not running"
      start    # 如果脚本没有跑，重新启动
   fi
#   python3 news_focusing_recommends_monitor.py  # 发送邮件
}

###################################
#(函数)停止程序
#
#说明：
#注意: 在shell编程中，"$?" 表示上一句命令或者一个函数的返回值
###################################
stop() {
   checkpid
   if [ "$?" -ne 0 ]; then
#   if [ ! -z "$?" ]; then
      echo "Stopping $PYTHON_FILE ...(psid=$PSID) "
      kill -9 $PSID

#      PSID=$(ps | grep $PYTHON_FILE| grep -v "grep" | awk '{print $1}')
      checkpid
      if [ "$?" -ne 0 ]; then
       echo "程序未能杀死，PSID：$PSID"
      else
        echo "[OK]"
      fi

   else
      echo "================================"
      echo "warning: $PYTHON_FILE is not running"
      echo "================================"
   fi
}


case "$DO" in
   'start')
     start
     ;;
   'stop')
     stop
     ;;
   'restart')
     stop
     start
     ;;
   'status')
     status
     ;;
  *)
     echo "Usage: sh $0 xx.py [start|stop|restart|status]"
     exit 1
esac

