#! /bin/bash

# Usage ./scripts/deploy.sh [ /path/to/docker-img-tarball docker-img-tag ]

set -eo pipefail

echo "✔ Begin deploying ..."

DOCKER_TARBALL=${1:-"smilecdr-2020.05.PRE-14-docker.tar.gz"}
DOCKER_REPO="kidsfirstdrc/smilecdr"
DOCKER_IMAGE_TAG=${DOCKER_TARBALL#"smilecdr-"}
DOCKER_IMAGE_TAG=${DOCKER_IMAGE_TAG%"-docker.tar.gz"}
DOCKER_IMAGE=${2:-"$DOCKER_REPO:$DOCKER_IMAGE_TAG"}

if [ $(docker image ls $DOCKER_IMAGE | wc -l) -eq 2 ]
then
    echo "Using docker image $DOCKER_IMAGE"
else
    if [[ ! -f $DOCKER_TARBALL ]]; then
        echo "Aborting! Cannot find docker image tarball $DOCKER_TARBALL"
        exit 1
    fi

    echo "Loading docker image from tarball: $DOCKER_TARBALL"
    docker image load --input=$DOCKER_TARBALL
    docker tag smilecdr:latest $DOCKER_IMAGE
fi

cd smilecdr
docker-compose down

if [[ ! -f '.env' ]]; then
    cp 'dev.env' '.env'
fi
docker-compose up -d --build

echo "Waiting for smilecdr docker stack to finish deploying (may take a few minutes) ..."
until docker-compose logs | grep -q "up and running"
do
    echo "."
    sleep 2
done

echo "✅ Finished deploying!"
