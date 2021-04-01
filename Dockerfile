FROM python:3.8

RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y gettext libgettextpo-dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /community_app

COPY Pipfile Pipfile.lock /community_app/
RUN pip install pipenv && pipenv install --system


COPY . /community_app/