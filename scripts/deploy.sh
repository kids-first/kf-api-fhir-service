#! /bin/bash

# Usage ./scripts/deploy.sh [ /path/to/docker-img-tarball docker-img-tag ]

set -eo pipefail

echo "✔ Begin deploying ..."

DOCKER_TARBALL=${1:-"smilecdr-2020.05.PRE-14-docker.tar.gz"}
DOCKER_HUB_USERNAME=${DOCKER_HUB_USERNAME}
DOCKER_HUB_PW=${DOCKER_HUB_PW}
DOCKER_REPO="kidsfirstdrc/smilecdr"
DOCKER_IMAGE_TAG=${DOCKER_TARBALL#"smilecdr-"}
DOCKER_IMAGE_TAG=${DOCKER_IMAGE_TAG%"-docker.tar.gz"}
DOCKER_IMAGE=${2:-"$DOCKER_REPO:$DOCKER_IMAGE_TAG"}

# Set env file
if [[ ! -f '.env' ]]; then
    cp 'dev.env' '.env'
fi

# Try using a local Smile CDR image if it exists
if [ "$(docker images -q $DOCKER_IMAGE 2> /dev/null)" != "" ]
then
    echo "Using docker image $DOCKER_IMAGE"
else
    # Try pulling the image from Docker Hub if it exists
    echo "Smile CDR docker image $DOCKER_IMAGE not found, try pulling from $DOCKER_REPO ..."
    if [[ -z $DOCKER_HUB_USERNAME ]] || [[ -z $DOCKER_HUB_PW ]]
    then
        source .env
    fi
    echo "Logging into Docker Hub ..."
    echo "$DOCKER_HUB_PW" | docker login -u "$DOCKER_HUB_USERNAME" --password-stdin
    docker pull $DOCKER_IMAGE

    # Try creating the image from a local tarball
    if [[ -f $DOCKER_TARBALL ]]; then
        echo "Loading docker image from tarball: $DOCKER_TARBALL"
        docker image load --input=$DOCKER_TARBALL
        docker tag smilecdr:latest $DOCKER_IMAGE
    fi
fi
# Could not fetch or find image - fail
if [ "$(docker images -q $DOCKER_IMAGE 2> /dev/null)" == "" ]; then
    echo "Aborting! Could not find or fetch the Smile CDR docker image."
    exit 1
fi

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
