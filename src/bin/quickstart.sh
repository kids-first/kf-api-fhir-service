#!/bin/bash

# Setup python virtual env with project dependencies
# Setup docker-compose stack
# Generate data 
# Load data 
# Seed smile cdr users 

# --- CLI Options ---

# --delete-volumes will delete any volumes in the docker-compose stack

set -e

START_TIME=$SECONDS
# DELETE_VOLUMES=0

while [ -n "$1" ]; do 
	case "$1" in
	--delete-volumes) DELETE_VOLUMES=1 ;; 
	*) echo "Option $1 not recognized" ;; 
	esac
	shift
done

if [ $DELETE_VOLUMES -eq 1 ]; then
    ./src/bin/setup_dev_env.sh --delete-volumes
else
    ./src/bin/setup_dev_env.sh
fi

if [ ! -d venv ]; then
echo "🐍 Setup Python virtual env and install deps ..."
    virtualenv venv
    source venv/bin/activate
    pip install -e .
else
    source venv/bin/activate
fi

echo "🏭 Generating sample data ..."
./src/bin/generate_data.py 2 5

echo "🔼 Load sample data ..."
./src/bin/load_data.py admin password 

echo "🔼 Seed Smile CDR users ..."
./src/bin/seed_users.py admin password smilecdr/settings/users.json

ELAPSED=$((( SECONDS - START_TIME ) / 60 ))
FORMATTED_ELAPSED=$(printf "%.2f" $ELAPSED)
echo ""
echo "Elapsed time $FORMATTED_ELAPSED minutes"

echo "✅ --- Quickstart setup complete! ---"

