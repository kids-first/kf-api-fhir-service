FROM 538745987955.dkr.ecr.us-east-1.amazonaws.com/kf-smile-cdr:2020.05.PRE-14 as test

WORKDIR /home/smile/smilecdr

COPY server/settings/master.properties classes/cdr-config-Master.properties
COPY server/settings/logback.xml classes/logback.xml
COPY server/settings/jvm.sh bin/setenv

# JVM max memory
ENV JVM_MAX_HEAP_SIZE -Xmx2048m
# Pretty print JSON
ENV FHIR_PRETTY_PRINT true
# Do not store full HTTP bodies in transaction db
ENV PERSIST_TRANSACTION_BODIES false
# Respect forwarded headers doesn't matter in test
ENV RESPECT_FWD_HEADERS false
# Load the full base FHIR model during server init
ENV SEED_CONF_RESOURCES true
# Use in memory database
ENV DB_DRIVER H2_EMBEDDED
ENV DB_CONN_URL jdbc:h2:file:./database/cdr
ENV DB_CDR_USERID admin
ENV DB_CDR_PASSWORD password

FROM 538745987955.dkr.ecr.us-east-1.amazonaws.com/kf-smile-cdr:2020.05.PRE-14 as production

# JVM max memory
ENV JVM_MAX_HEAP_SIZE -Xmx8g
# Respect forwarded headers from load balancer
ENV RESPECT_FWD_HEADERS true
# Use external Postgres database
ENV DB_DRIVER POSTGRES_9_4
ENV DB_CONN_URL jdbc:postgresql://postgres_cdr:5432/cdr
