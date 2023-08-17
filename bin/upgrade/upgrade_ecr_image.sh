#!/bin/bash

# Pushes a Smile CDR docker image to the appropriate repo on ECR
# Configured for either kf-strides or include

# NOTE: You must run awslogin and select either of the AWS profiles below 
# during the login process before running this script

set -e
START_TIME=$SECONDS

KIDSFIRST_PROJECT="kf-strides-smile-cdr"
INCLUDE_PROJECT="include-smile-cdr"

KF_AWS_PROFILE="Mgmt-Console-Devops-D3bCenter@232196027141"
INCLUDE_AWS_PROFILE="Mgmt-Console-Devops-include@373997854230"

set -e
if [[ -z $1  &&  -z $2 ]]; then
    echo "First specify one of the project names (e.g. $KIDSFIRST_PROJECT or $INCLUDE_PROJECT)"
    echo "Next specify the smilecdr version to use as an image tag (e.g. 2023.05.R02)"
    echo "Usage: ./bin/upgrade/upgrade_ecr_image.sh kf-strides-smile-cdr 2023.05.R02"
    exit 1
fi

function usage() {
    echo -n \
        "Usage: $(basename "$0")
Publish container images to Elastic Container Registry (ECR).

First specify one of the project names (e.g. $KIDSFIRST_PROJECT or $INCLUDE_PROJECT)
Next specify the smilecdr version to use as an image tag (e.g. 2023.05.R02)

Usage: 

./bin/upgrade/$(basename "$0") kf-strides-smile-cdr 2023.05.R02
"
}

PROJECT_NAME=$1
TAG=$2

if [[ $PROJECT_NAME == $KIDSFIRST_PROJECT ]]; then
    AWS_PROFILE=$KF_AWS_PROFILE
else
    AWS_PROFILE=$INCLUDE_AWS_PROFILE
fi

function amazon_ecr_login() {
    # Retrieves a temporary authorization token that can be used to access
    # Amazon ECR, along with the registry URL.
    read -r AUTHORIZATION_TOKEN ECR_REGISTRY \
        <<<"$(aws --profile="$AWS_PROFILE" --region="us-east-1" ecr get-authorization-token \
            --output "text" \
            --query "authorizationData[0].[authorizationToken, proxyEndpoint]")"

    # The authorization token is base64 encoded, and we need to strip the
    # protocol from the registry URL.
    AUTHORIZATION_TOKEN="$(echo "${AUTHORIZATION_TOKEN}" | base64 --decode)"
    ECR_REGISTRY="${ECR_REGISTRY##*://}"

    # Authenticate to the ECR registry. The authorization token is presented in
    # the format user:password.
    echo "${AUTHORIZATION_TOKEN##*:}" |
        docker login \
            --username "${AUTHORIZATION_TOKEN%%:*}" \
            --password-stdin "${ECR_REGISTRY}"
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    if [[ "${1:-}" == "--help" ]]; then
        usage
    else
        echo "👮🏻‍♀️ Logging into aws ecr ..."
        amazon_ecr_login
        echo "🐳 Tagging docker image ..."
        docker tag "kidsfirstdrc/smilecdr:${TAG}" \
            "${ECR_REGISTRY}/${PROJECT_NAME}:${TAG}"
        echo "🐳 Pushing image to ${ECR_REGISTRY}/${PROJECT_NAME}:${TAG}..."
        docker push "${ECR_REGISTRY}/${PROJECT_NAME}:${TAG}"
    fi
fi

ELAPSED=$((( SECONDS - START_TIME ) / 60 ))
FORMATTED_ELAPSED=$(printf "%.2f" $ELAPSED)

echo "✅ Push image complete"
echo "Elapsed time $FORMATTED_ELAPSED minutes"
