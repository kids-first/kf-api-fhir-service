#!/bin/bash

# Update the base Smile CDR image on AWS ECR and Dockerhub (Optional)
# Used when we receive new releases

# ------------ Environment Variables ------------
# DOCKER_HUB_USERNAME DOCKER_HUB_PW - if set, push to Dockerhub
# AWS_PROFILE_NAME - if set, will use profile to push to ECR

# Usage ./scripts/update_smilecdr.sh /path/to/docker-img-tarball [image tag]

set -eo pipefail

echo "✔ Begin updating Smile CDR image ..."

if [[ -z $1 ]];
then
    echo "❌ You must provide the path to the Smile CDR docker tarball " \
         "(e.g. smilecdr-2020.05.PRE-14-docker.tar.gz)"
    exit 1
fi

# Use supplied image tag or make one from the tarball
DOCKER_TARBALL_PATH=$1
DOCKER_TARBALL=$(basename $1)
DOCKER_REPO="232196027141.dkr.ecr.us-east-1.amazonaws.com/kf-strides-smile-cdr"
if [[ -z $2 ]];
then
    DOCKER_IMAGE_TAG=${DOCKER_TARBALL#"smilecdr-"}
    DOCKER_IMAGE_TAG=${DOCKER_IMAGE_TAG%"-docker.tar.gz"}
else
    DOCKER_IMAGE_TAG=$2
fi
DOCKER_IMAGE="$DOCKER_REPO:$DOCKER_IMAGE_TAG"

# Load the image from the tarball
echo "Loading docker image from tarball: $DOCKER_TARBALL_PATH"
docker image load --input="$DOCKER_TARBALL_PATH"
docker tag smilecdr:latest $DOCKER_IMAGE

# Push image to ECR
if [[ -n $AWS_PROFILE_NAME ]];
then
    # Use profile if supplied
    passwd=$(aws --profile="$AWS_PROFILE_NAME" ecr get-login --region us-east-1 | awk '{ print $6 }')
else
    passwd=$(aws ecr get-login --region us-east-1 | awk '{ print $6 }')
fi
echo "Pushing $DOCKER_IMAGE ..."
docker login -u AWS -p $passwd "$DOCKER_REPO"
docker push "$DOCKER_IMAGE"

# Push images to Dockerhub - if secrets are set in environment
if [[ -n $DOCKER_HUB_USERNAME ]] && [[ -n $DOCKER_HUB_PW ]];
then
    echo "$DOCKER_HUB_PW" | docker login -u "$DOCKER_HUB_USERNAME" --password-stdin

    DOCKER_REPO="kidsfirstdrc/smilecdr"
    DOCKER_IMAGE="$DOCKER_REPO:$DOCKER_IMAGE_TAG"

    echo "Pushing $DOCKER_IMAGE ..."
    docker tag smilecdr:latest $DOCKER_IMAGE
    docker push "$DOCKER_IMAGE"
fi

echo "✅ Finished updating Smile CDR images!"
