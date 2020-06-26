#! /bin/bash

# Usage ./scripts/load_model.sh [ my-git-branch ]

# -- Environment Variables --
# Defaults to values in kf-api-fhir-service/.env
# SMILE_CDR_BASE_URL - url of Smile CDR FHIR server
# SMILE_CDR_USERNAME - username to authenticate with before loading resources into server
# SMILE_CDR_PASSWORD - password to authenticate with before loading resources into server

set -eo pipefail

# Args
GIT_REPO_BRANCH=${1:-master}

# Vars
if [[ ! -f '.env' ]]; then
    cp 'server/settings/dev.env' '.env'
fi
source .env
BASE_URL=${SMILE_CDR_BASE_URL:-http://localhost:8000}
SERVER_UNAME=${SMILE_CDR_USERNAME:-$DB_USERNAME}
SERVER_PW=${SMILE_CDR_PASSWORD:-$DB_PASSWORD}
GIT_ORG="ncpi-fhir"
GIT_REPO="ncpi-api-fhir-service"

echo "Loading NCPI model $GIT_REPO:$GIT_REPO_BRANCH into server ..."

if [[ ! -d $GIT_REPO ]]; then
    # Git clone the model
    git clone "git@github.com:$GIT_ORG/$GIT_REPO.git"
    # Setup venv
    cd $GIT_REPO
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -e .
else
    cd $GIT_REPO
    source venv/bin/activate
fi

git checkout "$GIT_REPO_BRANCH"
git pull

# Publish model to server
fhirutil publish site_root/input/resources/terminology \
--base_url="$BASE_URL" --username="$SERVER_UNAME" --password="$SERVER_PW"

fhirutil publish site_root/input/resources/extensions \
--base_url="$BASE_URL" --username="$SERVER_UNAME" --password="$SERVER_PW"

fhirutil publish site_root/input/resources/profiles \
--base_url="$BASE_URL" --username="$SERVER_UNAME" --password="$SERVER_PW"

fhirutil publish site_root/input/resources/search \
--base_url="$BASE_URL" --username="$SERVER_UNAME" --password="$SERVER_PW"
