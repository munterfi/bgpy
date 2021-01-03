#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Name          :check.sh
# Description   :Starts the python main process which starts three different
#                background processes and exits normally. After 25 seconds the
#                log is checked.
# Author        :Merlin Unterfinger <info@munterfinger.ch>
# Date          :2021-01-03
# Version       :0.1.0
# Usage         :./check.sh
# Notes         :Runs as GitHub Action.
# Bash          :5.0.17
# =============================================================================

# Create tmp folder if not existing
mkdir -p tmp

# Flatten log
>tmp/bg.log

# Start main process
python3 bg_py/main.py &

# Monitor
sleep 25
ps au && echo '' && tail -n 30 tmp/bg.log
