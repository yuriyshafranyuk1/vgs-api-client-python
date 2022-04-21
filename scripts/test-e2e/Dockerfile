FROM python:3.9.2-slim-buster

ADD ./scripts/test-e2e /scripts
ADD ./tests /tests

ENTRYPOINT ["bash", "./scripts/run.sh"]