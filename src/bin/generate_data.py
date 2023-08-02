#!/usr/bin/env python

import os
import shutil
import json
import argparse
from pprint import pprint

from src.config import ROOT_DIR, DATA_DIR
from src import fhir_builder


def generate_data(n_studies, n_patients):
    """
    Generate FHIR resources for n_studies
        - n_patients Patients per Study
        - 1 Specimens per Patient
    """
    print(f"🏭 Generating FHIR resources for {n_studies} studies")

    # Remove old data
    shutil.rmtree(DATA_DIR, ignore_errors=True)
    os.makedirs(DATA_DIR)

    patients = []
    specimens = []
    for i in range(n_studies):
        print(f"Creating data for study {i}")
        # Make n_patients patients per study
        patients.extend(
            [
                fhir_builder.patient(f"PT-{i}-{pi}", f"SD-{i}")
                for pi in range(n_patients)
            ]
        )
        # Make 1 specimens per patient
        specimens.extend(
            [
                fhir_builder.specimen(
                    f"SP-{i}-{pi}", f"PT-{i}-{pi}", f"SD-{i}")
                for pi in range(n_patients)
            ]
        )
    for rtype, data in [("Patient", patients), ("Specimen", specimens)]:
        filepath = os.path.join(DATA_DIR, f"{rtype}.json")
        with open(filepath, "w") as json_file:
            json.dump(data, json_file, indent=2)

        print(f"⛑️ Wrote {len(data)} {rtype} to {filepath}")


def cli():
    """
    CLI for running this script
    """
    parser = argparse.ArgumentParser(
        description='Generate FHIR resource payloads'
    )
    parser.add_argument(
        "n_studies",
        type=int,
        help="Number of studies for which data will be generated",
    )
    parser.add_argument(
        "n_patients",
        type=int,
        help="Number of patients per study to generate",
    )
    args = parser.parse_args()

    generate_data(args.n_studies, args.n_patients)

    print("✅ FHIR data generation complete")


if __name__ == "__main__":
    cli()
