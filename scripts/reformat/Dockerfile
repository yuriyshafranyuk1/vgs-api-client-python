FROM python:3.9.2-slim-buster

RUN pip install black flake8 isort

WORKDIR /vgs-api-client/

ENTRYPOINT ["bash", "./scripts/reformat/run.sh"]
