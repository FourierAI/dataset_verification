FROM python:3.8

RUN mkdir /app
RUN mkdir /app/dataset_verification
COPY main.py /app/dataset_verification
WORKDIR /app/dataset_verification

