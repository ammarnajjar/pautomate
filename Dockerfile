# See https://hub.docker.com/r/library/python/
FROM python:3.8-slim-buster

LABEL Name=pautomate Version=0.0.1


RUN apt-get update && apt-get install -y --no-install-recommends \
	git=1:2.20.1-2 \
	wget=1.20.1-1.1 \
	gpg=2.2.12-1+deb10u1 \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

RUN wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.asc.gpg
RUN mv microsoft.asc.gpg /etc/apt/trusted.gpg.d/
RUN wget -q https://packages.microsoft.com/config/debian/9/prod.list
RUN mv prod.list /etc/apt/sources.list.d/microsoft-prod.list
RUN chown root:root /etc/apt/trusted.gpg.d/microsoft.asc.gpg
RUN chown root:root /etc/apt/sources.list.d/microsoft-prod.list

RUN apt-get update && apt-get install -y --no-install-recommends \
	apt-transport-https=1.8.2 \
	dotnet-sdk-3.0=3.0.100-1 \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*


WORKDIR /package
COPY . /package

RUN python3 -m pip install -e .

WORKDIR /ws
ENTRYPOINT [ "pautomate" ]
