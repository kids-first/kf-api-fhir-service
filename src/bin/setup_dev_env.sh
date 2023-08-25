#!/bin/bash

# Setup python virtual env with project dependencies
# Setup docker-compose stack

# --- CLI Options ---

# --delete-volumes will delete any volumes in the docker-compose stack

set -e

START_TIME=$SECONDS
DELETE_VOLUMES=0
GITHUB_USERNAME=${GITHUB_USERNAME}
GITHUB_PAT_SMILECDR=${GITHUB_PAT_SMILECDR}

while [ -n "$1" ]; do 
	case "$1" in
	--delete-volumes) DELETE_VOLUMES=1 ;; 
	*) echo "Option $1 not recognized" ;; 
	esac
	shift
done

echo "➡️  Begin development environment setup for Smile CDR 🤓 ..."

if [ ! -d venv ]; then
echo "🐍 Setup Python virtual env and install deps ..."
    virtualenv venv
    source venv/bin/activate
    pip install -e .
else
    source venv/bin/activate
fi

echo "🐳 Start docker-compose stack ..."

# Set env file
if [[ ! -f '.env' ]]; then
    cp 'env.sample' '.env'
fi
source .env

echo "🐳 Clean up docker stack from before ..."

# Delete docker volumes
if [ $DELETE_VOLUMES -eq 1 ]; then
    echo "🗑️ Bring down stack and remove old volumes ..."
    docker-compose down -v  
else
    docker-compose down
fi

# Check github packages registry creds 
if [[ -z $GITHUB_USERNAME ]] || [[ -z $GITHUB_PAT_SMILECDR ]]
then
    echo "🔐 You must have the GITHUB_USERNAME and GITHUB_PAT_SMILECDR environment variable set to "
    echo "continue. GITHUB_PAT_SMILECDR should contain a Github personal access token (classic)"
    echo "with the appropriate permissions for reading from the Github package registry"
    echo "See https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-with-a-personal-access-token-classic for details"
    echo "🛂 You will also need to be a collaborator on the repo in GHCR"
    echo "Please contact Natasha Singh singn4@chop.edu or Alex Lubneuski lubneuskia@chop.edu"
    exit 1
fi

echo "Logging into Github packages registry ..."
echo "$GITHUB_PAT_SMILECDR" | docker login ghcr.io -u "$GITHUB_USERNAME" --password-stdin

sleep 10

echo "🐳 Start docker-compose stack ..."
docker-compose pull --ignore-pull-failures
docker-compose up -d --build

echo "🔥 Waiting for fhir server to finish deploying (may take up to 10 minutes) ..."
until $(curl --output /dev/null --head --silent --fail $FHIR_ENDPOINT/endpoint-health)
do
    echo -n "."
    sleep 2
done

ELAPSED=$((( SECONDS - START_TIME ) / 60 ))
FORMATTED_ELAPSED=$(printf "%.2f" $ELAPSED)
echo ""
echo "Elapsed time $FORMATTED_ELAPSED minutes"

echo "✅ --- Development environment setup complete! ---"

