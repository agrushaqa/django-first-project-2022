CREATE DATABASE askme;
CREATE USER grusha WITH ENCRYPTED PASSWORD 'xxx';
ALTER ROLE grusha SET client_encoding TO 'utf8';
ALTER ROLE grusha SET default_transaction_isolation TO 'read committed';
ALTER ROLE grusha SET timezone TO 'UTC';
ALTER USER grusha WITH SUPERUSER;
GRANT CONNECT ON DATABASE askme TO grusha;
GRANT ALL PRIVILEGES ON DATABASE askme TO grusha;
GRANT ALL PRIVILEGES ON DATABASE askme TO postgres;
grant create on schema public to grusha;
grant usage on schema public to grusha;
GRANT postgres TO grusha;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO grusha;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO grusha;
GRANT ALL ON ALL TABLES IN SCHEMA public to grusha;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public to grusha;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to grusha;

