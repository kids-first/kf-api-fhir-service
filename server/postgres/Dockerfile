# Extend the postgres image provided by docker hub
FROM postgres:11.4-alpine
COPY ./init_postgresdb.sh /docker-entrypoint-initdb.d/init_postgresdb.sh
