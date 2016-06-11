#! /usr/bin/env bash

set -e

VIRTUALENV_CMD="virtualenv"
VIRTUALENV_NAME="acorvin_code_challenge"
REQUIREMENTS_FILE="python-requirements.txt"

# To ensure program isolation, this script runs the API and installs all
# necessary dependencies within a python virtual environment.
#
# The first step is to ensure that the virtualenv command is available.

hash $VIRTUALENV_CMD 2>/dev/null || {
  echo >&2 "virtualenv command is not abailable.  Aborting.";
  exit 1;
}

# Create the python virtual environment
$VIRTUALENV_CMD $VIRTUALENV_NAME

# Activate the virtual environment
source ./$VIRTUALENV_NAME/bin/activate

# Now install python requirements into the virtual environment
pip install -r $REQUIREMENTS_FILE
