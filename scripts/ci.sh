#!/usr/bin/env bash

set -e
set -x

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
ROOT_DIR="${DIR}/.."
cd cdk
npm ci
npm run lint
npm run test
npm run synth
npm run build
cd ..

get_abs_filename() {
  # $1 : relative filename
  echo "$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
}

# Create zip files for guardian/actions-riff-raff@v1 GHA

filename="main.py"
app_name="snyk-tag-monitor"
zip -FSj "${app_name}.zip" "$filename"
