FROM python:3.9.2-slim-buster

ARG PYPI_TOKEN
ARG LIB_VERSION

ENV PYPI_TOKEN=$PYPI_TOKEN
ENV LIB_VERSION=$LIB_VERSION

RUN pip install --upgrade build twine wheel setuptools --verbose

WORKDIR /src

ENTRYPOINT ["bash", "publish/build_and_publish.sh"]