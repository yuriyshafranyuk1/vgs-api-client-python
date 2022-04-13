FROM python:3.9.2-slim-buster

ADD . /lib

# set version valid version
RUN grep -lr XXX.YYY.ZZZ ./lib/src | xargs sed -i "s/XXX.YYY.ZZZ/0.0.1/g"

WORKDIR /lib/src/v1/
RUN python setup.py install

WORKDIR /lib/tests/v1/
RUN pip install -r test-requirements.txt

ENTRYPOINT ["./run_tests.sh"]