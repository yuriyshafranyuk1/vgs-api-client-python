#!/bin/bash

set -e

usage() { echo "Required env var '$1' is missing"; exit 1; }

[ -z "${ARTIFACT_REPOSITORY_TOKEN}" ] && usage "ARTIFACT_REPOSITORY_TOKEN" ;

twine upload -u __token__ -p "${ARTIFACT_REPOSITORY_TOKEN}" --verbose dist/*.whl