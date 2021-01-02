#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Name          :run.sh
# Description   :Starts the python main process which starts three different
#                background processes and exits normally. Then starts
#                monitoring the processes and log.
# Author        :Merlin Unterfinger <info@munterfinger.ch>
# Date          :2020-12-09
# Version       :0.1.0
# Usage         :./run.sh
# Notes         :Need to kill the plain process manually as it will run
#                forever in background.
# Bash          :5.0.17
# =============================================================================

# Create tmp folder if not existing
mkdir -p tmp

# Flatten log
>tmp/bg.log

# Start main process
python3 bg_py/main.py &

# Monitor
while :; do
    clear
    ps au && echo '' && tail -n 30 tmp/bg.log
    sleep 2
done
