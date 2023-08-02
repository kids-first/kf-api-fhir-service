#!/bin/bash

# Setup python virtual env with project dependencies
# Setup docker-compose stack

# --- CLI Options ---

# --delete-volumes will delete any volumes in the docker-compose stack

set -e

START_TIME=$SECONDS
DELETE_VOLUMES=0
DOCKER_HUB_USERNAME=${DOCKER_HUB_USERNAME}
DOCKER_HUB_PW=${DOCKER_HUB_PW}

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

# Check docker hub creds 
if [[ -z $DOCKER_HUB_USERNAME ]] || [[ -z $DOCKER_HUB_PW ]]
then
    echo "🔐 You need the Kids First DRC docker hub credentials to continue" 
    echo "Please contact the Github repo admins: natasha@d3b.center or meenchulkim@d3b.center" 
    exit 1
fi

echo "Logging into Docker Hub ..."
echo "$DOCKER_HUB_PW" | docker login -u "$DOCKER_HUB_USERNAME" --password-stdin

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

