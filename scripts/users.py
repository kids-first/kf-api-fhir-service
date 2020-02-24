"""
User migration script to load users from one smilecdr deployment into another
"""

import argparse
import os
import json

from utils import BASE_URL, send_request

ENDPOINT = os.path.join(BASE_URL, 'user-management')


def create_or_update(user_file, update=False):
    """
    Create or update the smilecdr user payloads in the JSON file, `user_file`

    If update=True, then replace current users using PUT. Otherwise create
    new users using POST
    """
    print(f'Processing user file: {user_file} ...')
    with open(user_file, 'r') as user_json:
        users = json.load(user_json)['users']

    method_name = 'put' if update else 'post'
    for user in users:
        url = f'{ENDPOINT}/{user["nodeId"]}/{user["moduleId"]}'

        if method_name == 'put':
            url = os.path.join(url, str(user.get('pid')))
        else:
            user.pop('id', None)

        response = send_request(method_name, url, json=user)

        if response.status_code in {200, 201}:
            user['pid'] = response.json()['pid']

    with open(user_file, 'w') as user_json:
        json.dump({'users': users}, user_json, **{'indent': 4})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'user_file', help='Path to a JSON file containing user '
        'payloads expected by smilecdr /user-management endpoint'
    )
    parser.add_argument(
        '--update', action='store_true',
        help='Update the users in the user file instead of create new ones'
    )
    args = parser.parse_args()

    create_or_update(args.user_file, update=args.update)
