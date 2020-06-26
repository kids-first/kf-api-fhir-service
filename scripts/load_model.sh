#! /bin/bash

# Usage ./scripts/load_model.sh [ my-git-branch ]

# -- Environment Variables --
# Defaults to values in kf-api-fhir-service/.env
# SMILE_CDR_BASE_URL - url of Smile CDR FHIR server
# SMILE_CDR_USERNAME - username to authenticate with before loading resources into server
# SMILE_CDR_PASSWORD - password to authenticate with before loading resources into server

set -eo pipefail

# Args
GIT_REPO_PATH=${1:-ncpi-fhir/ncpi-api-fhir-service}
GIT_REPO_BRANCH=${2:-master}

# Vars
if [[ ! -f '.env' ]]; then
    cp 'server/settings/dev.env' '.env'
fi
source .env

GIT_REPO=${GIT_REPO_PATH##*/}

echo "$GIT_REPO"
BASE_URL=${SMILE_CDR_BASE_URL:-http://localhost:8000}
SERVER_UNAME=${SMILE_CDR_USERNAME:-$DB_USERNAME}
SERVER_PW=${SMILE_CDR_PASSWORD:-$DB_PASSWORD}


echo "Loading NCPI model $GIT_REPO_PATH into server ..."

# Delete existing model
rm -rf $GIT_REPO

# Git clone the model
git clone "git@github.com:$GIT_REPO_PATH.git"
cd $GIT_REPO
git checkout "$GIT_REPO_BRANCH"

# Setup venv
if [[ ! -d "$(pwd)/$GIT_REPO/venv" ]]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -e .
fi
source venv/bin/activate

# Publish model to server
fhirutil publish site_root/input/resources/terminology \
--base_url="$BASE_URL" --username="$SERVER_UNAME" --password="$SERVER_PW"

fhirutil publish site_root/input/resources/extensions \
--base_url="$BASE_URL" --username="$SERVER_UNAME" --password="$SERVER_PW"

fhirutil publish site_root/input/resources/profiles \
--base_url="$BASE_URL" --username="$SERVER_UNAME" --password="$SERVER_PW"

fhirutil publish site_root/input/resources/search \
--base_url="$BASE_URL" --username="$SERVER_UNAME" --password="$SERVER_PW"
