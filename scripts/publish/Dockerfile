FROM python:3.9.2-slim-buster

RUN pip install --upgrade build twine wheel setuptools --verbose

WORKDIR /vgs-api-client/

ENTRYPOINT ["bash", "./scripts/publish/run.sh"]
