#!/usr/bin/env bash

set -ex

usage() { echo "Required env var '$1' is missing"; exit 1; }

[ -z "${LIB_VERSION}" ] && usage "LIB_VERSION" ;
[ -z "${ARTIFACT_REPOSITORY_TOKEN}" ] && usage "ARTIFACT_REPOSITORY_TOKEN" ;

docker-compose -f docker-compose.publish.yaml build build_and_publish
docker-compose -f docker-compose.publish.yaml run build_and_publish
