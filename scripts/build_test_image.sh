#!/bin/bash

# Create the Smile CDR docker image for integration tests
# The test Smile CDR image is built by snapshotting a running container built
# from the test build target. See Dockerfile for more details on the test
# build target

# It must be created this way in order to capture the base FHIR model
# which gets loaded into the server during container initialization

# Usage
# ./scripts/build_test_image.sh

set -eo pipefail


echo "✔ Begin building integration test image ..."

SMILE_CDR_VERSION=$(cat Dockerfile | grep -e "FROM .* as test" \
                    | cut -d " " -f2 | cut -d ":" -f2)
DOCKER_REPO='kidsfirstdrc/smilecdr'
DOCKER_TEST_IMAGE="$DOCKER_REPO:$SMILE_CDR_VERSION-test"
DOCKER_CONTAINER="fhir-test-server"

# Build the integration test server image
echo "Build integration test server image (will take ~20 minutes) ..."

echo "1) Deploying Smile CDR base server (~10 minutes) ..."
docker build --target test -t "$DOCKER_TEST_IMAGE" .
docker run -d --rm --name $DOCKER_CONTAINER -p 8000:8000 "$DOCKER_TEST_IMAGE"

# Wait for server to come up
until docker container logs $DOCKER_CONTAINER 2>&1 | grep "up and running"
do
    echo -n "."
    sleep 2
done

# Sanity check
curl -I -u admin:password http://localhost:8000/StructureDefinition/Patient

# Wait 10 min for ValueSet pre-expansion
echo "2) ✔ Deployed test server, waiting for ValueSet pre-expansion to finish (~10 minutes)"
end=$((SECONDS+600))
while [ $SECONDS -lt $end ]; do
    echo -n "."
    sleep 2
done

# Create new image from running container
echo "3) ✔ ValueSet pre-expansion complete, creating test server snapshot ..."
docker commit -c "ENV SEED_CONF_RESOURCES false" $DOCKER_CONTAINER "$DOCKER_TEST_IMAGE"
echo "$DOCKER_HUB_PW" | docker login -u "$DOCKER_HUB_USERNAME" --password-stdin
docker push "$DOCKER_TEST_IMAGE"
docker rm -f $DOCKER_CONTAINER

echo "✅ Completed build integration test image"
