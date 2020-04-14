#! /bin/bash

# Usage ./scripts/load_kidsfirst.sh [ my-git-branch --refresh ]

# --refresh flag forces a git fetch and hard reset on the Kids First model
# before loading

# -- Environment Variables --
# Defaults to values in kf-api-fhir-service/.env
# SMILE_CDR_BASE_URL - url of Smile CDR FHIR server
# SMILE_CDR_USERNAME - username to authenticate with before loading resources into server
# SMILE_CDR_PASSWORD - password to authenticate with before loading resources into server

set -eo pipefail

# Args
GIT_REPO_BRANCH=${1:-master}
REFRESH="$2"

# Vars
source smilecdr/.env
BASE_URL=${SMILE_CDR_BASE_URL:-http://localhost:8000}
SERVER_UNAME=${SMILE_CDR_USERNAME:-$DB_CDR_USERID}
SERVER_PW=${SMILE_CDR_PASSWORD:-$DB_CDR_PASSWORD}
GIT_REPO="kf-model-fhir"

echo "Loading Kids First model $GIT_REPO:$GIT_REPO_BRANCH into server ..."

if [[ ! -d $GIT_REPO ]]; then
    # Git clone kf-model-fhir
    git clone git@github.com:kids-first/kf-model-fhir.git
    # Setup venv
    cd $GIT_REPO
    python3 -m venv venv
    source venv/bin/activate
    pip install -e .
else
    cd $GIT_REPO
    source venv/bin/activate
fi

git checkout "$GIT_REPO_BRANCH"

# Refresh the Kids First FHIR model repo
if [[ $REFRESH = '--refresh' ]]; then
    echo "Refreshing $GIT_REPO:$GIT_REPO_BRANCH ..."
    git fetch
    git reset --hard origin/$GIT_REPO_BRANCH
fi

# Publish model to server
fhirmodel publish site_root/input/resources/terminology \
--base_url="$BASE_URL" --username="$SERVER_UNAME" --password="$SERVER_PW"

fhirmodel publish site_root/input/resources/extensions \
--base_url="$BASE_URL" --username="$SERVER_UNAME" --password="$SERVER_PW"

fhirmodel publish site_root/input/resources/profiles \
--base_url="$BASE_URL" --username="$SERVER_UNAME" --password="$SERVER_PW"

fhirmodel publish site_root/input/resources/search \
--base_url="$BASE_URL" --username="$SERVER_UNAME" --password="$SERVER_PW"

fhirmodel publish site_root/input/resources/examples \
--base_url="$BASE_URL" --username="$SERVER_UNAME" --password="$SERVER_PW"
