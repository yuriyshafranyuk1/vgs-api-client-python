#!/bin/bash

grep -rl XXX.YYY.ZZZ . | xargs sed -i "s/XXX.YYY.ZZZ/${LIB_VERSION}/g"

# Build
python setup.py sdist
python setup.py bdist_wheel

# Publish
twine upload -u __token__ -p "${PYPI_TOKEN}" --verbose dist/*.whl
