FROM python:3.9.2-slim-buster

ADD . /vgs-api-client

WORKDIR /vgs-api-client/

ENTRYPOINT ["bash", "./scripts/test/run.sh"]