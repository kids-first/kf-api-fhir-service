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
    USER_MGMNT_ENDPOINT,
    SEED_USERS_FILEPATH,
)


def add_authorization(user):
    # Extract consent authorizations and store in user.notes as JSON encoded str
    consent = user.get("auth_config", {})
    if consent:
        user["notes"] = json.dumps(consent)
    return user


def create_user(client_id, client_secret, endpoint, user):
    """
    Create Smile CDR user

    Return the response json if creation was successful
    Return None if creation failed due another user with the same
    username already existing
    Raise an exception if user creation fails for any other reason
    """
    headers = {
        "Content-Type": "application/json",
    }
    username = user['username']

    # Extract consent authorizations and store in user.notes as JSON encoded str
    user = add_authorization(user)
    try:
        resp = requests.post(
            endpoint,
            headers=headers,
            auth=HTTPBasicAuth(client_id, client_secret),
            json=user
        )
        resp.raise_for_status()
        result = resp.json()
        print(f"Created user {username}")
    except requests.exceptions.HTTPError as e:
        print(f"Failed to create user {username}")
        print("Problem sending request to FHIR server")
        print(resp.text)
        raise e

    return result


def seed_users(client_id, client_secret, seed_users_filepath):
    """
    Create or update Smile CDR users
    """
    with open(seed_users_filepath, "r") as json_file:
        data = json.load(json_file)

    headers = {
        "Content-Type": "application/json",
    }
    created_users = []
    for user in data:
        node_id = user.pop("nodeId")
        module_id = user.pop("moduleId")
        username = user['username']
        endpoint = f"{USER_MGMNT_ENDPOINT}/{node_id}/{module_id}"

        # Get user by username
        result = None
        try:
            resp = requests.get(
                f"{USER_MGMNT_ENDPOINT}/{node_id}/{module_id}?searchTerm={username}",
                headers=headers,
                auth=HTTPBasicAuth(client_id, client_secret),
            )
            resp.raise_for_status()
            result = resp.json().get("users", [])
            if len(result) > 0:
                result = result[0]
        except requests.exceptions.HTTPError as e:
            print(f"Failed to find user {user['username']}")
            print("Problem sending request to FHIR server")
            print(resp.text)
            if resp.status_code == 404:
                pass
            else:
                raise e

        # Update  user
        if result:
            print(f"Found existing user {result['username']}")
            # Extract consent authorizations and store in user.notes as JSON encoded str
            user = add_authorization(user)
            pid = result["pid"]
            try:
                resp = requests.put(
                    f"{USER_MGMNT_ENDPOINT}/{node_id}/{module_id}/{pid}",
                    headers=headers,
                    auth=HTTPBasicAuth(client_id, client_secret),
                    json=user
                )
                resp.raise_for_status()
                result = resp.json()
                print(f"Updated user {username} with pid {pid}")
            except requests.exceptions.HTTPError as e:
                print(f"Failed to update user {user['username']}")
                print("Problem sending request to FHIR server")
                print(resp.text)
                if "ConstraintViolationException" in resp.text:
                    update_pid = True
                else:
                    raise e
        # Create new user
        else:
            result = create_user(client_id, client_secret, endpoint, user)

        user.update(result)
        created_users.append(user)

    with open(seed_users_filepath, "w") as json_file:
        json.dump(created_users, json_file, indent=2)


def cli():
    """
    CLI for running this script
    """
    parser = argparse.ArgumentParser(
        description='Seed user data in FHIR server'
    )
    parser.add_argument(
        "client_id",
        help="Admin ID to authenticate with FHIR server",
    )
    parser.add_argument(
        "client_secret",
        help="Admin secret to authenticate with FHIR server",
    )
    parser.add_argument(
        "seed_users_filepath",
        default=SEED_USERS_FILEPATH,
        help="Path to file with Smile CDR users",
    )
    args = parser.parse_args()

    seed_users(args.client_id, args.client_secret, args.seed_users_filepath)

    print("✅ Seed user data complete")


if __name__ == "__main__":
    cli()
