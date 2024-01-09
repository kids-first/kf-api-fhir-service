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
    headers = {
        "Content-Type": "application/json",
    }
    try:
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
            pass
        else:
            raise e
    return result


def unlock_admin_with_backup(
    admin_backup_username="admin_backup", admin_backup_pw=FHIR_APP_ADMIN_PW
):
    """
    This is used to unlock the main admin account. Often times during
    deployment, the main admin account gets locked. We don't know why
    but we can unlock it with the backup admin account
    """
    username = FHIR_APP_ADMIN
    print(
        f"🔎 Searching for user: {username}"
    )
    # We must fetch the user to get its PID - required for update
    result = None
    try:
        result = get_user(
            f"{USER_MGMNT_ENDPOINT}/Master/local_security",
            username,
            admin_backup_username,
            admin_backup_pw,
        )
        if not result:
            print(
                f"❌ Could not unlock user '{username}' because"
                " user does not exist yet"
            )
            return
    except Exception as e:
        print(
            f"❌ Failed to unlock user '{username}'."
            f" User '{admin_backup_username}' may not exist yet or there is"
            " a problem with the password or the account is locked"
        )
        print(str(e))
    else:
        users = unlock_account(
            result, admin_backup_username, admin_backup_pw
        )
        pprint(users)
        print(f"✅ Unlock {username} complete")


def cli():
    """
    CLI for running this script
    """
    parser = argparse.ArgumentParser(
        description='Unlock admin user account'
    )
    parser.add_argument(
        "--admin_backup_username",
        default="admin_backup",
        help="Backup admin username",
    )
    parser.add_argument(
        "--admin_backup_pw",
        default=FHIR_APP_ADMIN_PW,
        help="Backup admin password",
    )
    args = parser.parse_args()

    # Unlock the account with backup admin
    unlock_admin_with_backup(args.admin_backup_username, args.admin_backup_pw)


if __name__ == "__main__":
    cli()
