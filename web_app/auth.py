#!/usr/bin/env python

import os
import json
import argparse
from pprint import pprint
from pathlib import Path

import requests
from requests.auth import HTTPBasicAuth
import jwt
from dotenv import find_dotenv, load_dotenv

DOTENV_PATH = find_dotenv()
if DOTENV_PATH:
    load_dotenv(DOTENV_PATH)

KEYCLOAK_HOST = os.environ.get("KEYCLOAK_HOST") or "localhost"
KEYCLOAK_PORT = os.environ.get("KEYCLOAK_PORT") or "8080"
KEYCLOAK_ISSUER = (
    os.environ.get("KEYCLOAK_ISSUER") or
    f"http://{KEYCLOAK_HOST}:{KEYCLOAK_PORT}/realms/fhir-dev"
)
KEYCLOAK_CLIENT_ID = (
    os.environ.get("KEYCLOAK_CLIENT_ID") or "fhir-superuser-client"
)
KEYCLOAK_CLIENT_SECRET = os.environ.get("KEYCLOAK_CLIENT_SECRET") or "none"
SMILECDR_HOST = os.environ.get("SMILECDR_HOST") or "localhost"
SMILECDR_PORT = os.environ.get("SMILECDR_PORT") or "8000"
SMILECDR_FHIR_ENDPOINT = "http://{SMILECDR_HOST}:{SMILECDR_PORT}"
SMILECDR_AUDIENCE = "https://kf-api-fhir-smilecdr-dev.org"


def send_request(method, *args, **kwargs):
    print("\n***** Sending request ******")
    print(args)
    pprint(kwargs)
    try:
        requests_op = getattr(requests, method)
        resp = requests_op(*args, **kwargs)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Problem sending request to endpoint")
        print(resp.text)
        raise e

    return resp


def get_access_token(
    client_id=KEYCLOAK_CLIENT_ID, client_secret=KEYCLOAK_CLIENT_SECRET,
    issuer=KEYCLOAK_ISSUER, decoded=True
):
    """
    Test OAuth2 stuff
    """
    headers = {
        "Content-Type": "application/json",
    }
    # Get OIDC configuration
    print("\n****** Get OIDC Configuration *************")
    openid_config_endpoint = (
        f"{issuer}/.well-known/openid-configuration"
    )
    resp = send_request("get", openid_config_endpoint, headers=headers)
    openid_config = resp.json()
    pprint(openid_config)

    # Authorize to get access token
    print("\n****** Get Access Token *************")
    token_endpoint = openid_config["token_endpoint"]
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": SMILECDR_AUDIENCE
    }
    params = {
        "scope": "fhir"
    }
    resp = send_request("post", token_endpoint, data=payload, params=params)
    token_payload = resp.json()
    access_token = token_payload["access_token"]
    pprint(token_payload)

    print("\n****** Introspect Token *************")
    decoded_token = jwt.decode(
        access_token, options={"verify_signature": False}
    )
    pprint(decoded_token)

    token_payload.update({
        "decoded_token": decoded_token
    })
    return token_payload


def cli():
    """
    CLI for running this script
    """
    parser = argparse.ArgumentParser(
        description='Get access token for client'
    )
    parser.add_argument(
        "--client_id",
        default=KEYCLOAK_CLIENT_ID,
        help="Keycloak Client ID",
    )
    parser.add_argument(
        "--client_secret",
        default=KEYCLOAK_CLIENT_SECRET,
        help="Keycloak Client secret",
    )
    parser.add_argument(
        "--issuer",
        default=KEYCLOAK_ISSUER,
        help="Keycloak Issuer URL",
    )
    args = parser.parse_args()

    get_access_token(args.client_id, args.client_secret, args.issuer)


if __name__ == "__main__":
    cli()
