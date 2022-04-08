FROM python:3.9.2-slim-buster

ADD . /src

# set version valid version
RUN grep -lr XXX.YYY.ZZZ ./src | xargs sed -i "s/XXX.YYY.ZZZ/0.0.1/g"

WORKDIR /src

RUN python setup.py install
RUN pip install -r test-requirements.txt

ENTRYPOINT ["pytest", "test/test_api.py"]