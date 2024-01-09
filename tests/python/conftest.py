from pprint import pprint

import pytest
from requests.auth import HTTPBasicAuth

from src.config import (
    FHIR_URL,
    USER_MGMNT_ENDPOINT,
    FHIR_APP_ADMIN,
    FHIR_APP_ADMIN_PW,
    FHIR_TEST_USER_PW
)
from src.bin.seed_users import upsert_users
from tests.python.utils import send_request


@pytest.fixture(scope="session")
def upsert_smilecdr_users():
    """
    Fixture that returns a function which upserts smilecdr basic auth users
    """
    upserted = []

    def _upsert_smilecdr_users(users):
        """
        Upsert list of user objects into smilecdr
        """
        # for user in users:
        #     user["accountLocked"] = False
        upserted.extend(
            upsert_users(
                FHIR_APP_ADMIN, FHIR_APP_ADMIN_PW, USER_MGMNT_ENDPOINT, users
            )
        )
        return upserted

    yield _upsert_smilecdr_users

    # -- Cleanup after fixture --

    # Disable users bc there is no API to delete users
    for user in upserted:
        user["authorities"] = []
        disabled_users = upsert_users(
            FHIR_APP_ADMIN, FHIR_APP_ADMIN_PW, USER_MGMNT_ENDPOINT, upserted
        )


@pytest.fixture(scope="session")
def fhir_superuser(upsert_smilecdr_users):
    """
    Create a FHIR super user in the smilecdr server
    """
    users = [
        {
            "username": f"ingest_client_{i}",
            "password": FHIR_TEST_USER_PW,
            "nodeId": "Master",
            "moduleId": "local_security",
            "authorities": [
                {
                    "permission": "ROLE_FHIR_CLIENT_SUPERUSER"
                }
            ],
        }
        for i in range(1)
    ]
    upserted = upsert_smilecdr_users(users)

    return upserted[0]


@pytest.fixture()
def upsert_fhir_resources():
    """
    Fixture that returns a function to upsert fhir resources in the server
    """
    upserted = []

    def _upsert_fhir_resources(resources):
        """
        Upsert some fhir resources in the server
        """
        kwargs = {"auth": HTTPBasicAuth(FHIR_APP_ADMIN, FHIR_APP_ADMIN_PW)}
        for resource in resources:
            id_ = resource["id"]
            resource_type = resource["resourceType"]
            url = f"{FHIR_URL}/{resource_type}/{id_}"
            kwargs.update({"json": resource})
            resp = send_request("put", url, **kwargs)

            upserted.append(resp.json())

        return upserted

    yield _upsert_fhir_resources

    # -- Cleanup after fixture --

    # Delete resources
    kwargs = {"auth": HTTPBasicAuth(FHIR_APP_ADMIN, FHIR_APP_ADMIN_PW)}
    for resource in upserted:
        id_ = resource["id"]
        resource_type = resource["resourceType"]
        url = f"{FHIR_URL}/{resource_type}/{id_}"
        kwargs.update({"json": resource})

        send_request("delete", url, **kwargs)


@pytest.fixture()
def patients(upsert_fhir_resources):
    """
    Fixture that upserts some patients in the server
    """
    resources = [
        {
            "resourceType": "Patient",
            "id": f"PT-{i}",
            "gender": "female",
        }
        for i in range(5)
    ]
    return upsert_fhir_resources(resources)
