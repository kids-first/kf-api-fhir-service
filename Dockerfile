FROM kidsfirstdrc/smilecdr:2020.05.PRE-14

WORKDIR /home/smile/smilecdr

COPY server/settings/master.properties classes/cdr-config-Master.properties
COPY server/settings/logback.xml classes/logback.xml
COPY server/settings/jvm.sh bin/setenv
