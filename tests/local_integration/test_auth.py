from pprint import pprint

import pytest
import requests
from requests.auth import HTTPBasicAuth

from src.config import (
    FHIR_URL, KEYCLOAK_CLIENT_ID, KEYCLOAK_CLIENT_SECRET, KEYCLOAK_TOKEN_URL
)

# Todo
# Move send_request to a tests/utils.py
# Create fixture for data
# Create fixture for smile cdr user
# Create helpers to load these into FHIR


def get_token(
    client_id=KEYCLOAK_CLIENT_ID, client_secret=KEYCLOAK_CLIENT_SECRET,
    token_url=KEYCLOAK_TOKEN_URL
):
    kwargs = {
        "json":
        {
            "client_id": client_id,
            "client_secret": client_secret,
        }
    }
    return send_request("post", token_url, **kwargs).json()["access_token"]


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


@pytest.mark.parametrize(
    "action,endpoint",
    [("get", "metadata"), ("get", "swagger-ui/")]
)
def test_anonymous_valid_actions(action, endpoint):
    """
    Test that anonymous user can GET /metadata and /swagger-ui
    """
    url = f"{FHIR_URL}/{endpoint}"
    resp = send_request(action, url)


@pytest.mark.parametrize(
    "action,endpoint",
    [("get", "Patient"), ("post", "Patient")]
)
def test_anonymous_invalid_actions(action, endpoint):
    """
    Test that anonymous user cannot do anything besides GET /metadata and
    GET /swagger-ui/
    """
    kwargs = {}
    if action == "post":
        patient = {
            "resourceType": "Patient",
            "gender": "male"
        }
        kwargs = {"json": patient}

    url = f"{FHIR_URL}/{endpoint}"

    with pytest.raises(requests.exceptions.HTTPError) as e:
        resp = send_request(action, url, **kwargs)
        assert resp.status_code == 403


def test_crud_with_basic_auth():
    """
    Test that basic auth user can CRUD FHIR resources
    since it has ROLE_FHIR_CLIENT_SUPERUSER
    """
    url = f"{FHIR_URL}/Patient"
    kwargs = {"auth": HTTPBasicAuth("ingest_client", "iamSmile123")}

    # Post
    patient = {
        "resourceType": "Patient",
        "gender": "male"
    }
    kwargs.update({"json": patient})
    resp = send_request("post", url, **kwargs)
    pid = resp.json()["id"]
    assert pid

    # Put
    patient["gender"] = "female"
    patient["id"] = pid
    resp = send_request("put", f"{url}/{pid}", **kwargs)

    # Get
    resp = send_request("get", f"{url}/{pid}", **kwargs)
    gender = resp.json()["gender"]
    assert gender == "female"

    # Delete
    resp = send_request("delete", f"{url}/{pid}", **kwargs)

    with pytest.raises(requests.exceptions.HTTPError):
        resp = send_request("get", f"{url}/{pid}", **kwargs)
        assert resp.status_code == 404


def test_crud_with_oidc_auth():
    """
    Test OIDC authed user can CRUD
    """
    access_token = get_token()
    kwargs = {
        "headers": {
            "Authorization": f"Bearer {access_token}"
        }
    }
    url = f"{FHIR_URL}/Patient"

    # Post
    patient = {
        "resourceType": "Patient",
        "gender": "male"
    }
    kwargs.update({"json": patient})
    resp = send_request("post", url, **kwargs)
    pid = resp.json()["id"]
    assert pid

    # Put
    patient["gender"] = "female"
    patient["id"] = pid
    resp = send_request("put", f"{url}/{pid}", **kwargs)

    # Get
    resp = send_request("get", f"{url}/{pid}", **kwargs)
    gender = resp.json()["gender"]
    assert gender == "female"

    # Delete
    resp = send_request("delete", f"{url}/{pid}", **kwargs)

    with pytest.raises(requests.exceptions.HTTPError):
        resp = send_request("get", f"{url}/{pid}", **kwargs)
        assert resp.status_code == 404
