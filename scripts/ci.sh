#!/usr/bin/env bash

set -e
set -x

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

( #Steps to package the python venv
  MAJOR_PYTHON_VERSION="3.9"
  PACKAGE_ROOT_DIR="${DIR}/.venv/lib/python${MAJOR_PYTHON_VERSION}/site-packages"
  ZIP_FILE="${APP_NAME}.zip"
  cp "${DIR}/main.py" "${PACKAGE_ROOT_DIR}"
  cd "${PACKAGE_ROOT_DIR}"
  zip -FSr ${ZIP_FILE} .
  mv "${PACKAGE_ROOT_DIR}/${ZIP_FILE}" "${DIR}/${ZIP_FILE}"
)
