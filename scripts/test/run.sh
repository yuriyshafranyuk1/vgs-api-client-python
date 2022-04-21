#!/usr/bin/env bash

set -e

echo "Installing lib from local sources"

# fix version
VERSION=0.0.1.dev$(date "+%Y%m%d%H%M")
grep -rl XXX.YYY.ZZZ . | xargs sed -i "s/XXX.YYY.ZZZ/$VERSION/g"

python setup.py install

pushd tests
  pip install -r test-requirements.txt
  echo "Running tests"
  pytest . -vvv --last-failed
popd