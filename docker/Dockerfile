FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /opt/code
WORKDIR /opt/code

ADD requirements.txt /opt
RUN pip install -r /opt/requirements.txt