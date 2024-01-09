#!/usr/bin/env python

# Unlock user account

# This is used to unlock the main admin account. Often times during
# deployment, the main admin account gets locked. We don't know why
# but we can unlock it with the backup

import argparse
from pprint import pprint, pformat

import requests
from requests.auth import HTTPBasicAuth

from src.config import (
    USER_MGMNT_ENDPOINT,
    FHIR_APP_ADMIN,
    FHIR_APP_ADMIN_PW
)

from src.bin.seed_users import upsert_users, get_user


def unlock_account(user, admin_username, admin_password):
    """
    Unlock account
    """
    pid = user["pid"]
    user.update({
        "accountLocked": False,
    })
    url = f"{USER_MGMNT_ENDPOINT}/Master/local_security/{pid}"

    result = None
    try:
        headers = {
            "Content-Type": "application/json",
        }
        resp = requests.put(
            url,
            headers=headers,
            auth=HTTPBasicAuth(admin_username, admin_password),
            json=user
        )
        resp.raise_for_status()
        result = resp.json()
        print(f"Updated user {user['username']} at {url}")
    except (
        requests.exceptions.HTTPError, requests.exceptions.JSONDecodeError
    ) as e:
        print(f"Failed to update user {user['username']} at {url}")
        print("Problem sending request to FHIR server")
        print(resp.text)
        if "ConstraintViolationException" in resp.text:
            update_pid = True
        else:
            raise e
    return result


def cli():
    """
    CLI for running this script
    """
    parser = argparse.ArgumentParser(
        description='Unlock user account'
    )
    parser.add_argument(
        "--username",
        help="Username to unlock",
    )
    parser.add_argument(
        "--admin_username",
        default="admin_backup",
        help="Admin username",
    )
    parser.add_argument(
        "--admin_password",
        default=FHIR_APP_ADMIN_PW,
        help="Admin password",
    )
    args = parser.parse_args()

    # Unlock the account with backup admin
    print(
        f"🔎 Searching for user: {args.username}"
    )
    result = get_user(
        f"{USER_MGMNT_ENDPOINT}/Master/local_security",
        args.username,
        FHIR_APP_ADMIN,
        FHIR_APP_ADMIN_PW,
    )
    if not result:
        print(
            f"❌ Could not unlock user '{args.username}' because"
            " user does not exist yet"
        )
    else:
        print(f"🔓 Attempting to unlock account {args.username}")
        users = unlock_account(
            result, args.admin_username, args.admin_password
        )
        pprint(users)
        print(f"✅ Unlock {args.username} complete")


if __name__ == "__main__":
    cli()
