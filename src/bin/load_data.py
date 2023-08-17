#!/usr/bin/env python

import os
import json
import argparse
import time
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from requests.auth import HTTPBasicAuth

from src.config import (
    DATA_DIR,
    FHIR_URL,
    FHIR_APP_ADMIN,
    FHIR_APP_ADMIN_PW
)
from src.misc import elapsed_time_hms

RESOURCE_LOAD_ORDER = [
    "Patient",
    "Specimen"
]


def do_put(base_url, endpoint, headers, username, password, resource):
    """
    Helper function to PUT FHIR resource
    """
    url = f"{base_url}/{endpoint}/{resource['id']}"

    try:
        print(f"Upserting {endpoint} {resource['id']}")
        resp = requests.put(
            url,
            headers=headers,
            auth=HTTPBasicAuth(username, password),
            json=resource
        )
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Problem sending request to FHIR server")
        print(resp.text)
        raise e
    return f"PUT {FHIR_URL}/{endpoint}/{resource['id']}"


def load_data(username, password, use_async=False):
    """
    Load test data into FHIR server
    """
    headers = {
        "Content-Type": "application/json",
    }
    start_time = time.time()
    for resource_type in RESOURCE_LOAD_ORDER:
        filename = f"{resource_type}.json"
        filepath = os.path.join(DATA_DIR, filename)
        if not os.path.exists(filepath):
            print(f"Skipping {filepath}, does not exist")
            continue
        with open(filepath, "r") as json_file:
            data = json.load(json_file)
        endpoint = filename.split(".")[0]

        if use_async:
            print("⚡️ Using async loading ...")
            with ThreadPoolExecutor() as tpex:
                futures = []
                for i, resource in enumerate(data):
                    futures.append(
                        tpex.submit(do_put, FHIR_URL, endpoint, headers,
                                    username, password, resource)
                    )
                for f in as_completed(futures):
                    print(f.result())
                    pass
        else:
            for i, resource in enumerate(data):
                do_put(
                    FHIR_URL, endpoint, headers,
                    username, password, resource
                )
    print(f"\nElapsed time (hh:mm:ss): {elapsed_time_hms(start_time)}\n")


def cli():
    """
    CLI for running this script
    """
    parser = argparse.ArgumentParser(
        description='Load data into FHIR server'
    )
    parser.add_argument(
        "--username",
        default=FHIR_APP_ADMIN,
        help="Username to authenticate with FHIR server",
    )
    parser.add_argument(
        "--password",
        default=FHIR_APP_ADMIN_PW,
        help="Password to authenticate with FHIR server",
    )
    parser.add_argument(
        "--use_async",
        action="store_true",
        help="Use async loading to update FHIR server",
    )
    args = parser.parse_args()

    load_data(args.username, args.password, args.use_async)

    print("✅ Load data complete")


if __name__ == "__main__":
    cli()
