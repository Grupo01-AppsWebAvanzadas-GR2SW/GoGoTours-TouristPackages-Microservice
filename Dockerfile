FROM tiangolo/uvicorn-gunicorn:python3.11
LABEL authors="Churukun"
LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./src /app