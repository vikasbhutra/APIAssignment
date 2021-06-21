FROM python:3.9.4-slim

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
    && apt-get -y install netcat gcc postgresql \
    && apt-get clean

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .