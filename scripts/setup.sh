#!/usr/bin/env bash

set -e

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
ROOT_DIR="${DIR}/.."

python3 -m venv "$ROOT_DIR/.venv"
source "$ROOT_DIR/.venv/bin/activate"

pip3 install -r "$ROOT_DIR/requirements.txt"