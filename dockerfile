FROM python:3 as ezgen

EXPOSE 8015
RUN mkdir /opt/app
WORKDIR /opt/app

COPY config.json core.py EzGen.py requirements.txt ./
COPY source ./source/
RUN pip3 install -r requirements.txt