#!/usr/bin/env bash

docker-compose -f docker-compose.test.yaml build test
docker-compose -f docker-compose.test.yaml run test
