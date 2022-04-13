#!/usr/bin/env bash

docker-compose -f docker-compose.tests.yaml build test
docker-compose -f docker-compose.tests.yaml run test
