#!/bin/bash

# Create a new Smile CDR docker image from a smilecdr tar.gz release
# ./bin/upgrade/new_image.sh <path to tar.gz> <docker image tag>

set -e
START_TIME=$SECONDS

if [[ -z $1 && -z $2 ]];
then
    echo "You must supply the path to the docker tar.gz and the image tag to use"
    echo "Usage: ./bin/$(basename "$0") path/to/tar.gz kidsfirstdrc:smilecdr/2023.05.R02"
    exit 1
fi

echo "📦 Loading image from $1 ..."
docker load < "$1" 

echo "🏷️ Tagging image with $2"
docker tag smilecdr:latest "$2"


ELAPSED=$((( SECONDS - START_TIME ) / 60 ))
FORMATTED_ELAPSED=$(printf "%.2f" $ELAPSED)
echo "✅ Created new image. Remember to update docker-compose.yml"
echo "Elapsed time $FORMATTED_ELAPSED minutes"

