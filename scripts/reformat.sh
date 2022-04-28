#!/bin/bash

set -e

docker-compose build reformat && \
docker-compose run reformat
