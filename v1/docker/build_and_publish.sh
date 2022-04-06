#!/bin/bash

# Build
python setup.py sdist
python setup.py bdist_wheel

# Publish
twine upload -u __token__ -p "${PYPI_TOKEN}" --verbose dist/*.whl
