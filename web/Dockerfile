FROM alpine:3.17

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

RUN apk update && apk add libffi-dev python3-dev gcc libc-dev
RUN apk add py3-pip py3-psycopg2 uwsgi uwsgi-python3 uwsgi-http postgresql-client

ADD . /usr/src/app
WORKDIR /usr/src/app

RUN adduser -D artem
USER artem

COPY --chown=artem:artem requirements.txt requirements.txt
COPY --chown=artem:artem start start
RUN chmod 777 start

ENV PATH="/home/artem/.local/bin:${PATH}"

RUN pip3 install --upgrade pip
RUN pip3 install --user -r requirements.txt

COPY --chown=artem:artem . .
