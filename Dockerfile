FROM python:2.7-alpine
LABEL maintainer "Andrew Ekstedt <ekstedta@oregonstate.edu>"

RUN pip install gunicorn

COPY requirements.txt /src/requirements.txt
RUN apk update \
    && apk add build-base openssl-dev libffi-dev curl \
    && pip install -r /src/requirements.txt  \
    && apk add openssl libffi \
    && apk del build-base openssl-dev libffi-dev

COPY ["setup.py", "/src/"]
COPY ["metaxe/__init__.py", "metaxe/app.py", "metaxe/api.py", "/src/metaxe/"]
COPY ["metaxe/templates", "/src/metaxe/templates/"]
RUN pip install -e /src

ENV METAXE_CONFIG /src/config.py
ENV TZ America/Los_Angeles
USER nobody
HEALTHCHECK CMD curl -fsS http://localhost:8000/healthcheck || exit 1
CMD ["gunicorn", "--bind", ":8000", "metaxe.app:app"]
