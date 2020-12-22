FROM python:3.8.1-slim-buster
ARG alphavantage_api_key

RUN apt-get update
RUN apt-get -y install cron
RUN apt-get -y install curl
RUN apt-get -y install procps
RUN apt-get -y install iputils-ping
RUN apt-get -y install vim

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY src/predictor /app/predictor
COPY data /app/data

RUN chown 664 /app/data

ENV ALPHAVANTAGE_API_KEY=$alphavantage_api_key
ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD cd /app/predictor && python ./main.py

