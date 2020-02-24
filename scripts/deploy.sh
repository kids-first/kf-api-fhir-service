#! /bin/bash

# Usage ./scripts/deploy.sh [ --refresh ]

# See scripts/load_kidsfirst.sh for environment variable and argument
# descriptions

set -eo pipefail

echo "✔ Begin deploying ..."

#DOCKER_IMAGE="smilecdr-2019.11.R01-docker.tar.gz"
DOCKER_IMAGE="smilecdr-2020.02.R01-docker.tar.gz"

if [[ ! -f $DOCKER_IMAGE ]]; then
    echo "Aborting! Cannot find docker image $DOCKER_IMAGE"
fi

if docker images | grep -w "smilecdr"
then
    echo "Using docker image $DOCKER_IMAGE"
else
    echo "Loading docker image from $DOCKER_IMAGE"
    docker image load --input=$DOCKER_IMAGE
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

cd ..
echo "Loading Kids First FHIR model into server ..."
./scripts/load_kidsfirst.sh "$@"
echo "✅ Finished deploying!"
