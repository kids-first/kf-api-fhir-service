
from pprint import pprint

import requests
from requests.auth import HTTPBasicAuth

from src.config import (
    KEYCLOAK_CLIENT_ID,
    KEYCLOAK_CLIENT_SECRET,
    KEYCLOAK_ISSUER,
    KEYCLOAK_PROXY_URL
)


def get_token(
    client_id=KEYCLOAK_CLIENT_ID, client_secret=KEYCLOAK_CLIENT_SECRET,
):
    # If running locally, go through the Keycloak proxy to get token
    # bc we cannot get the token directly from Keycloak
    # running in the docker network
    if KEYCLOAK_ISSUER.startswith("http://keycloak"):
        return get_token_from_proxy(client_id, client_secret)

    # Normal OIDC client credentials flow if running with a publicly
    # accessible Keycloak
    token_url = f"{KEYCLOAK_ISSUER}/protocol/openid-connect/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    params = {
        "scope": "fhir"
    }
    resp = send_request("post", token_url, data=payload, params=params)
    token_payload = resp.json()

    return token_payload["access_token"]


def get_token_from_proxy(
    client_id=KEYCLOAK_CLIENT_ID, client_secret=KEYCLOAK_CLIENT_SECRET,
):
    payload = {
        "kwargs": {
            "data":
            {
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            },
        },
        "http_operation": "post",
        "endpoint": f"{KEYCLOAK_ISSUER}/protocol/openid-connect/token"
    }
    return send_request(
        "post", KEYCLOAK_PROXY_URL, json=payload
    ).json()["access_token"]


def send_request(method, *args, **kwargs):
    try:
        requests_op = getattr(requests, method.lower())
        resp = requests_op(*args, **kwargs)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Problem sending request to endpoint. Args, Kwargs:")
        print(args)
        pprint(kwargs)
        print(resp.text)
        raise e

    return resp
