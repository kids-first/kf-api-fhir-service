#!/bin/bash set -e

#POSTGRES_USER, POSTGRES_DB and POSTGRES_PASSWORD are environment variables defined by the parent postgres image.
#POSTGRES_USER is the DB superuser, POSTGRES_PASSWORD is superuser's password and POSTGRES_DB is the default DB.
#POSTGRES_USER and POSTGRES_DB both default to "postgres". POSTGRES_PASSWORD is blank by default.
#All three variables can be overridden by environment settings.
#The script below creates only a single DB for Smile CDR with name $FHIR_DB_NAME with a single user ID and password "$FHIR_USER_LOGIN" and "$FHIR_PASSWORD"
#Additional CREATE and GRANT statements can be included if additional databases and/or user ids are required.


psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<- EOSQL
CREATE ROLE $FHIR_DB_USERNAME LOGIN password '$FHIR_DB_PASSWORD';
CREATE DATABASE $FHIR_DB_NAME;
CREATE DATABASE $FHIR_AUDIT_DB_NAME;
GRANT ALL PRIVILEGES ON DATABASE $FHIR_DB_NAME TO $FHIR_DB_USERNAME;
GRANT ALL PRIVILEGES ON DATABASE $FHIR_AUDIT_DB_NAME TO $FHIR_DB_USERNAME;
EOSQL
