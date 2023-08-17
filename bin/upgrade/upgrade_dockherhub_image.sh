#!/bin/bash

# Push new smilecdr image to Dockherhub

# ./bin/upgrade/upgrade_dockerhub_image.sh <docker image tag>

set -e
START_TIME=$SECONDS
DOCKER_HUB_USERNAME=${DOCKER_HUB_USERNAME}
DOCKER_HUB_PW=${DOCKER_HUB_PW}

if [[ -z $1 ]];
then
    echo "You must supply image tag to push"
    echo "Usage: ./bin/upgrade/$(basename "$0") kidsfirstdrc:smilecdr/2023.05.R02"
    exit 1
fi

echo "🐳 Logging into Docker Hub ..."
echo "$DOCKER_HUB_PW" | docker login -u "$DOCKER_HUB_USERNAME" --password-stdin

echo "🐳 Pushing image to $2 ..."
docker push "$2"

ELAPSED=$((( SECONDS - START_TIME ) / 60 ))
FORMATTED_ELAPSED=$(printf "%.2f" $ELAPSED)
echo "✅ Push image complete. Remember to update docker-compose.yml"
echo "Elapsed time $FORMATTED_ELAPSED minutes"

