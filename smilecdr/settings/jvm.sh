#!/bin/bash

# Use the JVMARGS property to set any JVM arguments which will be
# passed to the JVM when starting Smile CDR. These can be used to
# tune memory use, etc.

JVM_MAX_HEAP_SIZE=${JVM_MAX_HEAP_SIZE:-"-Xmx4g"}

# Only set the JVMARGS if not already set by the caller
if [ -z "$JVMARGS" ]; then

  JVMARGS="-server"

  # Set the maximum heap size for the JVM. Set this according to the
  # capacity of the server you will be deploying to and the load you
  # are anticipating needing to support. The default value of 4g
  # means 4 GB and is suitable for normal development server loads.
  # Production servers, servers with real loads, or servers that
  # process large amounts of data will almost certainly need more.
  JVMARGS="$JVMARGS $JVM_MAX_HEAP_SIZE"

  # If you are deploying to a cloud host, you might want to override the JVM
  # timezone to match the timezone where the system admins will be located (this
  # setting affects log files, etc
  #JVMARGS="$JVMARGS -Duser.timezone=America/New_York"

  # Useful for JDK 8 but not recommended for JDK 11+
  # JVMARGS="$JVMARGS -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled"

  # Some other good settings for a server
  JVMARGS="$JVMARGS -Dsun.net.inetaddr.ttl=60"
  JVMARGS="$JVMARGS -Djava.security.egd=file:/dev/./urandom"

fi

# This setting is used to determine the name of the file which will
# be read to obtain the node configuration. For example, if CONFIGNAME
# is set to "Master", Smile CDR will attempt to load configuration
# from a file in "classes/cdr-config-Master.properties"
if [ -z "$CONFIGNAME" ]; then
  CONFIGNAME=Master
fi

# These JVM arguments are passed to the startup/shutdown monitor process,
# which only runs for a short period of time during system startup and
# shutdown in order to provide feedback to the console
if [ -z "$WATCHJVMARGS" ]; then
  WATCHJVMARGS="-Xmx500m"
fi
JVMARGS="$JVMARGS -Dorg.xerial.snappy.use.systemlib=true"
