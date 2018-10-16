FROM python:2-slim

COPY requirements .
RUN apt-get update -q && apt-get install -y gcc && apt-get clean
RUN python -m pip install --upgrade pip
RUN python -m pip install --upgrade --user -r requirements
