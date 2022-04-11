FROM python:3.9.2-slim-buster

RUN pip install --upgrade build twine wheel setuptools --verbose

ADD . /lib
WORKDIR /lib/

CMD ["bash", "publish/build_and_publish.sh"]
