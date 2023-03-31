# pull official base image
FROM python:3.10.1-slim-buster

# set working directory
WORKDIR /usr/src/app

# set environment variables
# PYTHONDONTWRITEBYTECODE - prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED - prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update 

# install dependencies
# RUN pip install --upgrade pip
RUN /usr/local/bin/python -m pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .

CMD hypercorn --config "file:hypercorn_conf.py" main:app  

# CMD gunicorn -c gunicorn.conf.py wsgi:app
