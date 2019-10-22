# See https://hub.docker.com/r/library/python/
FROM python:3.7.2-slim-stretch

LABEL Name=pautomate Version=0.0.1


RUN apt-get update && apt-get install -y git wget gpg

RUN wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.asc.gpg
RUN mv microsoft.asc.gpg /etc/apt/trusted.gpg.d/
RUN wget -q https://packages.microsoft.com/config/debian/9/prod.list
RUN mv prod.list /etc/apt/sources.list.d/microsoft-prod.list
RUN chown root:root /etc/apt/trusted.gpg.d/microsoft.asc.gpg
RUN chown root:root /etc/apt/sources.list.d/microsoft-prod.list

RUN apt-get install -y apt-transport-https
RUN apt-get update
RUN apt-get install -y dotnet-sdk-2.2

WORKDIR /.package
ADD . /.package

# Using pip:
RUN python3.7 -m pip install -e .

WORKDIR /ws
ENTRYPOINT [ "pautomate" ]
