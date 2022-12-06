#!/usr/bin/env bash

set -e

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
ROOT_DIR="${DIR}/.."
APP_NAME="snyk-tag-monitor"
( #CDK build step
  cd "${ROOT_DIR}"/cdk
  npm ci
  npm run lint
  npm run test
  npm run synth
  npm run build
)

python3 -m venv "$ROOT_DIR/.venv"
source "$ROOT_DIR/.venv/bin/activate"

pip3 install -r "$ROOT_DIR/requirements.txt"

( #Steps to package the python venv
  MAJOR_PYTHON_VERSION="3.9"
  PACKAGE_DIR="${ROOT_DIR}/.venv/lib/python${MAJOR_PYTHON_VERSION}/site-packages"
  ZIP_FILE="${APP_NAME}.zip"

  cp "${ROOT_DIR}/main.py" "${PACKAGE_DIR}"
  cd "${PACKAGE_DIR}"
  zip -FSr "${ROOT_DIR}/${ZIP_FILE}" .
)
