
import pytest
import requests
from requests.auth import HTTPBasicAuth

from src.config import (
    FHIR_URL,
    KEYCLOAK_READ_CLIENT_ID,
    KEYCLOAK_READ_CLIENT_SECRET,
)
from tests.utils import send_request, get_token


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


def test_crud_with_basic_auth(fhir_superuser):
    """
    Test that basic auth user can CRUD FHIR resources
    since it has ROLE_FHIR_CLIENT_SUPERUSER
    """
    username = fhir_superuser["username"]
    password = fhir_superuser["password"]
    url = f"{FHIR_URL}/Patient"
    kwargs = {"auth": HTTPBasicAuth(username, password)}

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


def test_read_only_oidc_client(patients):
    """
    Test that a client with a read only role may view but not mutate
    any resources on the FHIR server
    """
    access_token = get_token(
        client_id=KEYCLOAK_READ_CLIENT_ID,
        client_secret=KEYCLOAK_READ_CLIENT_SECRET
    )
    kwargs = {
        "headers": {
            "Authorization": f"Bearer {access_token}"
        }
    }
    url = f"{FHIR_URL}/Patient"

    # Post - Fail
    patient = {
        "resourceType": "Patient",
        "gender": "male"
    }
    kwargs.update({"json": patient})
    with pytest.raises(requests.exceptions.HTTPError):
        resp = send_request("post", url, **kwargs)
        assert resp.status_code == 403

    # Put - Fail
    patient = patients[0]
    pid = patient["id"]
    patient["gender"] = "female"
    with pytest.raises(requests.exceptions.HTTPError):
        resp = send_request("put", f"{url}/{pid}", **kwargs)
        assert resp.status_code == 403

    # Get - Success
    resp = send_request("get", f"{url}/{pid}", **kwargs)
    assert resp.json()

    # Delete - Fail
    with pytest.raises(requests.exceptions.HTTPError):
        resp = send_request("delete", f"{url}/{pid}", **kwargs)
        assert resp.status_code == 403
