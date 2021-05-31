# Dockerfile
FROM ubuntu:18.04
FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y tesseract-ocr-eng
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]