#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Name          :run.sh
# Description   :Starts the python main process which starts three different
#                background processes and exits normally. Then starts
#                monitoring the processes and log.
# Author        :u228298 <merlin.unterfinger@sbb.ch>
# Date          :2020-11-30
# Version       :0.1.0
# Usage         :./run.sh
# Notes         :Need to kill the plain process manually as it will run
#                forever in background.
# Bash          :5.0.17
# =============================================================================

# Flatten log
>bg_py.log

# Start main process
python3 bg_py/main.py &

# Monitor
while :; do
    clear
    ps au && echo '' && tail -n 30 bg_py.log
    sleep 2
done
