#!/bin/bash

# Check FHIR endpoint health 

set -e

START_TIME=$SECONDS
FHIR_ENDPOINT=http://localhost:8000

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

