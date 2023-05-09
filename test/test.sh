#!/bin/bash

# Basic tests to ensure server is running corrrectly

source .env
source venv/bin/activate

# --- Test anonymous user ---
curl -X GET -o /dev/null -s --fail $FHIR_ENDPOINT/Patient
patient_access=$?
curl -X GET -o /dev/null -s --fail $FHIR_ENDPOINT/swagger-ui/
swagger_access=$?

if [ $patient_access -ne 0 ] && [ $swagger_access -eq 0 ]; then
  echo "Passed anonymous user test"
else
  echo "Failed anonymous user test"
  exit 1
fi

# --- Test basic auth ---
curl -X GET -u foo:bar -o /dev/null -s --fail $FHIR_ENDPOINT/Patient
patient_access_unknown=$?

curl -X GET -u ingest_client:iamSmile123 -o /dev/null -s --fail $FHIR_ENDPOINT/Patient
patient_access=$?


if [ $patient_access_unknown -ne 0 ] && [ $patient_access -eq 0 ]; then
  echo "Passed basic auth user test"
else
  echo "Failed basic auth user test"
  exit 1
fi

