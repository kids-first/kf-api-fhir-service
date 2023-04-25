#!/usr/bin/env python

import os
import json
import argparse
import time
from pprint import pprint

import requests
from requests.auth import HTTPBasicAuth

from src.config import (
    DATA_DIR,
    FHIR_URL
)
from src.misc import elapsed_time_hms


def load_data(client_id, client_secret):
    """
    Load test data into FHIR server
    """
    headers = {
        "Content-Type": "application/json",
    }
    start_time = time.time()
    for filename in os.listdir(DATA_DIR):
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, "r") as json_file:
            data = json.load(json_file)
        endpoint = filename.split(".")[0]

        for i, resource in enumerate(data):
            try:
                print(f"Upserting {endpoint} {resource['id']}")
                resp = requests.put(
                    f"{FHIR_URL}/{endpoint}/{resource['id']}",
                    headers=headers,
                    auth=HTTPBasicAuth(client_id, client_secret),
                    json=resource
                )
                resp.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print("Problem sending request to FHIR server")
                print(resp.text)
                raise e
    print(f"\nElapsed time (hh:mm:ss): {elapsed_time_hms(start_time)}\n")


def cli():
    """
    CLI for running this script
    """
    parser = argparse.ArgumentParser(
        description='Load data into FHIR server'
    )
    parser.add_argument(
        "client_id",
        help="Client ID to authenticate with FHIR server",
    )
    parser.add_argument(
        "client_secret",
        help="Client secret to authenticate with FHIR server",
    )
    args = parser.parse_args()

    load_data(args.client_id, args.client_secret)

    print("✅ Load data complete")


if __name__ == "__main__":
    cli()
