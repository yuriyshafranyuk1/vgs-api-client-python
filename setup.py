import os

from setuptools import setup

VERSION = os.environ.get("LIB_VERSION", "XXX.YYY.ZZZ")

setup(version=VERSION)
