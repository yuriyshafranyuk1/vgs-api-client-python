#!/usr/bin/env bash

set -e

if [[ -n "${LIB_VERSION}" ]]; then
  echo "Installing lib from PyPI ${LIB_VERSION} ..."

  set +e
  ATTEMPT=1
  while [  $ATTEMPT -lt 60 ]; do
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
else
  echo "Installing lib from local sources"
  python setup.py install
fi

pushd tests
  pip install -r test-requirements.txt
  pytest . -vvv --last-failed
popd