#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Name          :checks.sh
# Description   :Script for running all package (pytest, coverage, mypy and
#                flake8) checks.
# Author        :Merlin Unterfinger <info@munterfinger.ch>
# Date          :2021-01-18
# Version       :0.1.0
# Usage         :./checks.sh
# Notes         :
# Bash          :5.1.4
# =============================================================================

echo '*** pytest: Tests and coverage ***'
poetry run pytest --cov=bgpy tests/

echo -e '\n*** mypy: Static type checks ***'
poetry run mypy --config-file pyproject.toml .

echo -e '\n*** flake8: Code linting ***'
poetry run flake8 . --count --exit-zero --max-complexity=10 --statistics

echo -e '\n*** Building documentation ***'
cd docs && poetry run make html && cd ..
