#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Name          :install.sh
# Description   :Build the package wheel and install to global python of the
#                system.
# Author        :Merlin Unterfinger <info@munterfinger.ch>
# Date          :2021-01-18
# Version       :0.3.0
# Usage         :./install.sh
# Notes         :
# Bash          :5.1.4
# =============================================================================

echo '*** Setting up local env ***'
poetry install

echo -e '\n*** Building wheel ***'
rm -rf dist && poetry build

echo -e "\n*** Installing globally ($(which python3)) ***"
cd dist && python3 -m pip install --force-reinstall *.whl
