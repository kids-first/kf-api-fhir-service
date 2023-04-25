# ------ Environment variables ------

# The following env variables will be overwritten by values in the
# S3 secrets/app.env files at the time of deployment:

# Set the max memory for the JVM server process
# JVM_MAX_HEAP_SIZE

# Whether to load the full base FHIR model during server init
# SEED_CONF_RESOURCES

# Whether to validate resources against FHIR spec AND base profiles
# REQUEST_VALIDATION

# Whether server should respect forwarded headers 
# RESPECT_FWD_HEADERS

# Postgres configuration
# FHIR_DB_HOST
# FHIR_DB_USERNAME
# FHIR_DB_PASSWORD

# ------ Integration Test Server Image ------
# FROM 232196027141.dkr.ecr.us-east-1.amazonaws.com/kf-strides-smile-cdr:2021.02.R05 as test
FROM kidsfirstdrc/smilecdr:2023.02.R02 as test

WORKDIR /home/smile/smilecdr

# Use quickstart dev server settings
COPY smilecdr/settings/server-quickstart.properties classes/cdr-config-Master.properties
COPY smilecdr/settings/jvm.sh bin/setenv
COPY smilecdr/settings/system-users.json classes/config_seeding/users.json

# NOTE: 
# Test image uses in memory H2 database. 
# DB config is hardcoded in server-quickstart.properties

ENV JVM_MAX_HEAP_SIZE -Xmx4g
ENV SEED_CONF_RESOURCES false
ENV REQUEST_VALIDATION false
ENV RESPECT_FWD_HEADERS false

# ------ Production Server Image ------
FROM test as production
RUN apt update

# Use production server settings
COPY smilecdr/settings/server-postgres.properties classes/cdr-config-Master.properties

# JVM max memory - 8GB
ENV JVM_MAX_HEAP_SIZE -Xmx8g
ENV SEED_CONF_RESOURCES true
ENV REQUEST_VALIDATION true
ENV RESPECT_FWD_HEADERS true
ENV FHIR_DB_HOST localhost
ENV FHIR_DB_PORT 5432
ENV FHIR_DB_NAME cdr
ENV FHIR_AUDIT_DB_NAME audit
ENV FHIR_DB_USERNAME admin
ENV FHIR_DB_PASSWORD password

