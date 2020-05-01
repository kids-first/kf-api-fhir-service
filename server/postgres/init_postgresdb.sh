#!/bin/bash set -e

#POSTGRES_USER, POSTGRES_DB and POSTGRES_PASSWORD are environment variables defined by the parent postgres image.
#POSTGRES_USER is the DB superuser, POSTGRES_PASSWORD is superuser's password and POSTGRES_DB is the default DB.
#POSTGRES_USER and POSTGRES_DB both default to "postgres". POSTGRES_PASSWORD is blank by default.
#All three variables can be overridden by environment settings.
#The script below creates only a single DB for Smile CDR with name $CDR_DB_NAME with a single user ID and password "$CDR_USER_LOGIN" and "$CDR_PASSWORD"
#Additional CREATE and GRANT statements can be included if additional databases and/or user ids are required.

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<- EOSQL
CREATE ROLE $CDR_USER LOGIN password '$CDR_PASSWORD';
CREATE DATABASE $CDR_DB_NAME;
GRANT ALL PRIVILEGES ON DATABASE $CDR_DB_NAME TO $CDR_USER;
EOSQL
