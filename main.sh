#!/bin/bash

LOGFILE="log/start_stop.log"

cleanup() {
    echo "STOP:  $(date '+%Y/%m/%d %H:%M:%S') status=${1}" >> ${LOGFILE}
    exit $1
}

echo "START:" $(date "+%Y/%m/%d %H:%M:%S") >> ${LOGFILE}

trap 'cleanup 130' INT  # 130はSIGINTによる終了コード
trap 'cleanup 143' TERM # 143はSIGTERMによる終了コード

./lls2env/bin/python3 src/main.py
status=$?

cleanup $status