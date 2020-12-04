#!/usr/bin/env bash
# ----------------------------------------------------------------------------- 
# Name          :print_log.sh
# Description   :       
# Author        :u228298 <merlin.unterfinger@sbb.ch>
# Date          :2020-11-30
# Version       :0.1.0  
# Usage         :./print_log.sh
# Notes         :       
# Bash          :5.0.17 
# =============================================================================

watch "ps au && echo '' && tail -n 30 bgp.log"

