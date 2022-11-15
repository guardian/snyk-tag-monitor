#!/usr/bin/env bash

set -e
set -x

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
ROOT_DIR="${DIR}/.."
(
  cd "${ROOT_DIR}"/cdk
  npm ci
  npm run lint
  npm run test
  npm run synth
  npm run build
)

filename="main.py"
app_name="snyk-tag-monitor"
zip -FSj "${app_name}.zip" "$filename"
