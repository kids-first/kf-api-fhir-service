#!/usr/bin/env python

# Create a backup admin user

import argparse

from src.config import (
    USER_MGMNT_ENDPOINT,
    FHIR_APP_ADMIN,
    FHIR_APP_ADMIN_PW
)

from src.bin.seed_users import upsert_users


def upsert_admin(username, password):
    """
    Upsert a backup admin user
    """
    users = [
        {
            "username": username,
            "password": password,
            "nodeId": "Master",
            "moduleId": "local_security",
            "authorities": [
                {
                    "permission": "ROLE_SUPERUSER"
                }
            ],
        }
    ]
    users = upsert_users(
        FHIR_APP_ADMIN, FHIR_APP_ADMIN_PW, USER_MGMNT_ENDPOINT, users
    )

    return users


def cli():
    """
    CLI for running this script
    """
    parser = argparse.ArgumentParser(
        description='Create backup admin user'
    )
    parser.add_argument(
        "--username",
        default="admin_backup",
        help="Admin username",
    )
    parser.add_argument(
        "--password",
        default=FHIR_APP_ADMIN_PW,
        help="Admin password",
    )
    args = parser.parse_args()

    upsert_admin(
        args.username, args.password
    )

    print("✅ Upsert admin backup complete")


if __name__ == "__main__":
    cli()
