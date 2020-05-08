#! /bin/bash

# Usage ./scripts/deploy.sh [ /path/to/docker-img-tarball docker-img-tag ]

set -eo pipefail

echo "✔ Begin deploying ..."

DOCKER_HUB_USERNAME=${DOCKER_HUB_USERNAME}
DOCKER_HUB_PW=${DOCKER_HUB_PW}

# Set env file
if [[ ! -f '.env' ]]; then
    cp 'server/settings/dev.env' '.env'
fi

# Login to Dockerhub to fetch private smilecdr image
if [[ -z $DOCKER_HUB_USERNAME ]] || [[ -z $DOCKER_HUB_PW ]]
then
    source .env
fi
echo "Logging into Docker Hub ..."
echo "$DOCKER_HUB_PW" | docker login -u "$DOCKER_HUB_USERNAME" --password-stdin

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
