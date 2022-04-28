#!/bin/bash

set -e

black --exclude src/vgs_api_client/ . && \
flake . && \
isort -c .
