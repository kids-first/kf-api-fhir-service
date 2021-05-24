#!/bin/bash

# Update the base Smile CDR image on AWS ECR and Dockerhub (Optional)
# Used when we receive new releases

# ------------ Environment Variables ------------
# DOCKER_HUB_USERNAME DOCKER_HUB_PW - if set, push to Dockerhub
# AWS_PROFILE_NAME - if set, will use profile to push to ECR

# Usage ./scripts/update_smilecdr.sh /path/to/docker-img-tarball [aws cli version] [image tag]

set -eo pipefail

echo "⏳ Begin updating Smile CDR image ..."

if [[ -z $1 ]];
then
    echo "❌ You must provide the path to the Smile CDR docker tarball " \
         "(e.g. smilecdr-2020.05.PRE-14-docker.tar.gz)"
    exit 1
fi

# Configure AWS CLI version 
# AWS CLI version 1 will soon be deprecated, so when not provided, it defaults to 2
AWS_CLIENT_VERSION=${2:-"2"}
if [[ $AWS_CLIENT_VERSION != "1" ]] && [[ $AWS_CLIENT_VERSION != "2" ]];
then
    echo "❌ You must provide a valid AWS CLI version (e.g. 1 or 2)"
    exit 1
fi

# Use supplied image tag or make one from the tarball
DOCKER_TARBALL_PATH=$1
DOCKER_TARBALL=$(basename $1)
DOCKER_REPO="232196027141.dkr.ecr.us-east-1.amazonaws.com/kf-strides-smile-cdr"
if [[ -z $3 ]];
then
    DOCKER_IMAGE_TAG=${DOCKER_TARBALL#"smilecdr-"}
    DOCKER_IMAGE_TAG=${DOCKER_IMAGE_TAG%"-docker.tar.gz"}
else
    DOCKER_IMAGE_TAG=$3
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
    if [[ $AWS_CLIENT_VERSION == "1" ]];
    then
        passwd=$(aws --profile="$AWS_PROFILE_NAME" ecr get-login --region us-east-1 | awk '{ print $6 }')
    else
        passwd=$(aws --profile="$AWS_PROFILE_NAME" --region us-east-1 ecr get-login-password)
    fi
else
    if [[ $AWS_CLIENT_VERSION == "1" ]];
    then
        passwd=$(aws ecr get-login --region us-east-1 | awk '{ print $6 }')
    else
        passwd=$(aws --region us-east-1 ecr get-login-password)
    fi
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
