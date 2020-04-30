#!/bin/bash

# Abort the script if there is a non-zero error
set -eo pipefail

echo "✔ Begin building service image ..."

DOCKER_HUB_USERNAME=${DOCKER_HUB_USERNAME}
DOCKER_HUB_PW=${DOCKER_HUB_PW}

# Set env file
if [[ ! -f '.env' ]]; then
    cp 'server/settings/dev.env' '.env'
fi

# Login to Dockerhub to fetch private smilecdr image
echo "Smile CDR docker image $DOCKER_IMAGE not found, try pulling from $DOCKER_REPO ..."
if [[ -z $DOCKER_HUB_USERNAME ]] || [[ -z $DOCKER_HUB_PW ]]
then
    source .env
fi
echo "Logging into Docker Hub ..."
echo "$DOCKER_HUB_PW" | docker login -u "$DOCKER_HUB_USERNAME" --password-stdin

# Build KF FHIR service image
docker build -t kf-api-fhir-service:latest .

echo "✅ Finished building"
