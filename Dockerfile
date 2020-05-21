FROM 538745987955.dkr.ecr.us-east-1.amazonaws.com/kf-smile-cdr:2020.05.PRE-14

WORKDIR /home/smile/smilecdr

# JVM max memory
ENV JVM_MAX_HEAP_SIZE -Xmx8g
# Do not pretty print JSON
ENV FHIR_PRETTY_PRINT false
# Do not store full HTTP bodies in transaction db
ENV PERSIST_TRANSACTION_BODIES false
# Respect forwarded headers from load balancer
ENV RESPECT_FWD_HEADERS true
# Load the full base FHIR model during server init
ENV SEED_CONF_RESOURCES true

COPY server/settings/master.properties classes/cdr-config-Master.properties
COPY server/settings/logback.xml classes/logback.xml
COPY server/settings/jvm.sh bin/setenv
