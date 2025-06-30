#!/bin/bash

LOGFILE="log/start_stop.log"
PIDS=()

cleanup() {
    echo "STOP:  $(date '+%Y/%m/%d %H:%M:%S') status=${1}" >> ${LOGFILE}

    for pid in ${PIDS[@]}; do
        kill $pid 2>/dev/null
    done

    exit $1
}

echo "START:" $(date "+%Y/%m/%d %H:%M:%S") >> ${LOGFILE}

trap 'cleanup 130' INT  # 130はSIGINTによる終了コード
trap 'cleanup 143' TERM # 143はSIGTERMによる終了コード

./lls2env/bin/python3 src/main.py &
PIDS+=($!)

./lls2env/bin/python3 src/weekly_report.py &
PIDS+=($!)

./lls2env/bin/python3 src/monthly_reset.py &
PIDS+=($!)

wait "${PIDS[@]}"
cleanup $status