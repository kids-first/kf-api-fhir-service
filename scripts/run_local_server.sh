#! /bin/bash

# Usage ./scripts/deploy.sh [ /path/to/docker-img-tarball docker-img-tag ]

set -eo pipefail

echo "✔ Begin deploying ..."

# Build service container
source ./scripts/build.sh

# Destroy existing docker containers
docker-compose down

# Create and start all services (FHIR server, Postgres, Data Dashboard)
docker-compose pull --ignore-pull-failures
docker-compose up -d --build

echo "Waiting for smilecdr docker stack to finish deploying (may take a few minutes) ..."
until docker-compose logs | grep "up and running"
do
    echo "."
    sleep 2
done

echo "✅ Finished deploying!"
