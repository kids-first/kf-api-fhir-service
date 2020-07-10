#! /bin/bash

# Usage ./scripts/generate_synthetic_data.sh

set -eo pipefail


echo "✔ Begin generating synthetic patient data ..."

# Constants
ROOT_DIR=$(pwd)
DATA_DIR="synthetic-data"

SEED=12345
CLINICIAN_SEED=987
AGE_RANGE="0-18"
MODULE_FILTER="covid19"
EXPORT_FHIR_R4=true
EXPORT_FHIR_BULK_DATA=true


echo "Downloading the binary distribution of Synthea"

if [[ ! -f 'synthea-with-dependencies.jar' ]]; then
    wget https://github.com/synthetichealth/synthea/releases/download/master-branch-latest/synthea-with-dependencies.jar
fi


echo "Generating synthetic patient data ..."

i=0
while IFS=$'\t' read -r state column_1 population_size column_3 column_4
do
    test $i -eq 0 && ((i = i + 1)) && continue

    if [ $population_size -eq 0 ]; then
        echo "Skipping $state due to 0 population ..." && continue 
    fi

    echo "Generating $population_size patients in $state ..."

    java -jar synthea-with-dependencies.jar "$state" \
        -s $SEED \
        -cs $CLINICIAN_SEED \
        -p $population_size \
        -a $AGE_RANGE \
        -m $MODULE_FILTER \
        --exporter.fhir.export=$EXPORT_FHIR_R4 \
        --exporter.fhir.bulk_data=$EXPORT_FHIR_BULK_DATA \
        --exporter.baseDirectory "${ROOT_DIR}/${DATA_DIR}/${state}"  

done < "${ROOT_DIR}/scripts/hospitalizations.tsv"


echo "✅ Done generating synthetic patient data!"