#!/bin/bash

# Pushes a Smile CDR docker image to the appropriate repo on Github packages
# registry

# ./bin/upgrade/upgrade_ghcr_image.sh <docker image tag> <github username>

set -e
START_TIME=$SECONDS

if [[ -z $GITHUB_PAT_SMILECDR ]];
then
    echo "You must have the GITHUB_PAT_SMILECDR environment variable set to "
    echo "continue. This should contain a Github personal access token (classic)"
    echo "with the appropriate permissions for writing to Github package registry"
    echo "See https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-with-a-personal-access-token-classic for details"
fi


if [[ -z $1 && -z $2 ]];
then
    echo "You must supply the image tag to use and your github username"
    echo "Usage: ./bin/$(basename "$0") kids-first/smilecdr:2023.05.R02 znatty22"
    exit 1
fi

echo "🏷️ Tagging image with $1"
docker tag smilecdr:latest "ghcr.io/$1"

echo "🐳 Docker login to Github package registry ghcr.io"
echo $GITHUB_PAT_SMILECDR | docker login ghcr.io -u $2 --password-stdin

echo "🐳 Docker push to Github package registry"
docker push "ghcr.io/$1"

ELAPSED=$((( SECONDS - START_TIME ) / 60 ))
FORMATTED_ELAPSED=$(printf "%.2f" $ELAPSED)
echo "✅ Created new image. Remember to update docker-compose.yml"
echo "Elapsed time $FORMATTED_ELAPSED minutes"

