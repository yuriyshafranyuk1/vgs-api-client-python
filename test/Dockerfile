FROM python:3.9.2-slim-buster

ADD . /lib

# set version valid version
RUN grep -lr XXX.YYY.ZZZ ./lib/src | xargs sed -i "s/XXX.YYY.ZZZ/0.0.1/g"

WORKDIR /lib/src/vgs_api_client/v1/

RUN python setup.py install
RUN pip install -r test-requirements.txt

WORKDIR /lib/

ENTRYPOINT ["pytest", "test/test_api.py"]