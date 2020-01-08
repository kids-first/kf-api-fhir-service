#! /bin/bash

# Usage ./scripts/load_kidsfirst.sh [ --refresh ]

# --refresh flag forces a git pull on the Kids First model before loading

# -- Environment Variables --
# SMILE_CDR_BASE_URL - url of Smile CDR FHIR server
# SMILE_CDR_USERNAME - username to authenticate with before loading resources into server
# SMILE_CDR_PASSWORD - password to authenticate with before loading resources into server

set -eo pipefail

# Args
REFRESH="$1"

# Vars
source smilecdr/.env
BASE_URL=${SMILE_CDR_BASE_URL:-http://localhost:8000}
SERVER_UNAME=${SMILE_CDR_USERNAME:-$DB_CDR_USERID}
SERVER_PW=${SMILE_CDR_PASSWORD:-$DB_CDR_PASSWORD}
GIT_REPO="kf-model-fhir"

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

# Refresh the Kids First FHIR model repo
if [[ $REFRESH = '--refresh' ]]; then
    echo "Refreshing $GIT_REPO ..."
    git pull
fi

# ****** Temporary - Remove once master is updated *******
git checkout add-phenopackets-model

# Publish model to server
fhirmodel publish site_root/source/resources \
--base_url="$BASE_URL" --username="$SERVER_UNAME" --password="$SERVER_PW"
