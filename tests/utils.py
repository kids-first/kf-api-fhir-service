
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
