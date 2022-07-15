#!/usr/bin/env bash

set -e

echo "Installing lib from PyPI ${LIB_VERSION} ..."

set +e
ATTEMPT=1
while [  $ATTEMPT -lt 10 ]; do
  echo "Attempt ${ATTEMPT} ..."

  pip install vgs-api-client==${LIB_VERSION}

  if [[ $? == 0 ]]; then
    echo "Installed ${LIB_VERSION}"
    break
  fi

  ATTEMPT=$((ATTEMPT+1))

  sleep 5
done
set -e

pushd tests
  pip install -r test-requirements.txt
  echo "Running tests"
  pytest . -vvv --last-failed
popd

echo "Running examples"
for category in $(ls examples/); do
  for example in $(ls examples/$category/); do
    pushd examples/$category
      python $example
    popd
  done
done
