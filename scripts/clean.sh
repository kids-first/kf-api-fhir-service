#! /bin/bash

# Usage ./scripts/clean.sh

# Delete the smilecdr docker stack
# Deletes all images, containers, network, and volumes (data)

set -eo pipefail

docker-compose down --remove-orphans -v --rmi all
