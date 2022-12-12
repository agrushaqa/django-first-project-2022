FROM postgres:latest
USER root
RUN apt-get update
RUN apt-get install -y postgresql-14-wal2json
ADD docker-entrypoint-initdb.d/first_table.sql /docker-entrypoint-initdb.d/
RUN ls /docker-entrypoint-initdb.d
RUN chown postgres:postgres /docker-entrypoint-initdb.d/first_table.sql
RUN mkdir -p /var/lib/pgsql/data/pgdata/data