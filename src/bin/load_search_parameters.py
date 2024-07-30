#!/usr/bin/env python

import os
import argparse
from pprint import pprint

from requests.auth import HTTPBasicAuth

from src.config import (
    SEARCH_PARAMETER_DIR,
    REINDEX_PAYLOAD,
    BASE_URL,
    REINDEX_ENDPOINT,
    FHIR_APP_ADMIN,
    FHIR_APP_ADMIN_PW
)
from src.misc import (
    read_json,
    send_request
)


def upsert_search_parameters(
    client_id, client_secret, search_parameter_dir=SEARCH_PARAMETER_DIR
):
    """
    Read search parameters from file, then upsert them in server
    Last, reindex the resources so that SearchParameters take effect
    """
    print("Loading search parameters")

    for fn in os.listdir(search_parameter_dir):
        if not fn.endswith(".json"):
            continue
        filepath = os.path.join(search_parameter_dir, fn)
        search_param = read_json(filepath)

        # Load search parameter
        id_ = search_param["id"]
        endpoint = "/".join(
            part.strip("/") for part in [BASE_URL, "SearchParameter", id_]
        )
        resp = send_request(
            "put",
            endpoint,
            json=search_param,
            auth=HTTPBasicAuth(client_id, client_secret),
        )
        print(
            f"PUT {endpoint}"
        )

    # Start reindexing operation
    endpoint = f"{BASE_URL}/$reindex"
    resp = send_request(
        "post",
        endpoint,
        json=REINDEX_PAYLOAD,
        auth=HTTPBasicAuth(client_id, client_secret),
    )
    pprint(resp.json())


def cli():
    """
    CLI for running this script
    """
    parser = argparse.ArgumentParser(
        description='Load SearchParameters in FHIR server'
    )
    parser.add_argument(
        "--client_id",
        default=FHIR_APP_ADMIN,
        help="Admin ID to authenticate with FHIR server",
    )
    parser.add_argument(
        "--client_secret",
        default=FHIR_APP_ADMIN_PW,
        help="Admin secret to authenticate with FHIR server",
    )
    parser.add_argument(
        "--search_parameter_dir",
        default=SEARCH_PARAMETER_DIR,
        help="Path to dir with SearchParameters",
    )
    args = parser.parse_args()

    upsert_search_parameters(
        args.client_id, args.client_secret, args.search_parameter_dir
    )

    print("✅ Load SearchParameters complete")


if __name__ == "__main__":
    cli()
