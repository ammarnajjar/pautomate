# See https://hub.docker.com/r/library/python/
FROM python:3.8-slim-buster

LABEL Name=pautomate Version=0.0.1

WORKDIR /package
ADD . /package
RUN python3 -m pip install -e .

WORKDIR /ws
ENTRYPOINT [ "pautomate" ]
