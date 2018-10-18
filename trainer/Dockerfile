FROM python:2-slim

RUN apt-get update -q && apt-get install -y gcc && apt-get clean
RUN python -m pip install --upgrade pip
COPY requirements .
RUN python -m pip install --upgrade --user -r requirements
