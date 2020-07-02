#!/bin/bash

# Fetches file from S3 secrets bucket and optionally updates it if --update is
# provided as last arg

# Usage
# ./scripts/s3_secrets.sh [ dev | qa | prd ] s3-obj-rel-path /path/to/.env [ --update | --fetch ]

# Examples
# Update
# ./scripts/s3_secrets.sh dev kf-api-fhir-service/secrets.env secrets.env --update
# Fetch
# ./scripts/s3_secrets.sh dev kf-api-fhir-service/users.dev.json

set -e

DEPLOY_ENV="$1"
S3_REL_PATH="$2"
ENV_FILE="$3"
OPERATION=${4:-"--fetch"}
S3_BUCKET="s3://kf-538745987955-us-east-1-$DEPLOY_ENV-secrets"
S3_OBJ_PATH="$S3_BUCKET/$S3_REL_PATH"

if [[ -z $DEPLOY_ENV ]] || [[ -z $S3_REL_PATH ]]; then
    if [[ "$OPERATION" == '--update' &&  -z $ENV_FILE ]]; then
        echo "You must supply the following required args: "\
        "deploy environment (e.g. dev, qa, or prd), the relative S3 path "\
        "(e.g. kf-ui-fhir-data-dashboard/secrets.env), and path to the .env file."
        exit 1
    else
        echo "You must supply the following required args: "\
        "deploy environment (e.g. dev, qa, or prd), and the relative S3 path "\
        "(e.g. kf-ui-fhir-data-dashboard/secrets.env)"
        exit 1
    fi
fi

if [[ $OPERATION == '--update' ]];
then
    echo "Update $S3_OBJ_PATH with new file: $ENV_FILE ..."
    aws --profile=saml s3 cp "$ENV_FILE" "$S3_OBJ_PATH"
else
    echo "Fetch $S3_OBJ_PATH ..."
    aws --profile=saml s3 cp "$S3_OBJ_PATH" "$ENV_FILE"
fi
