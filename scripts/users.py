"""
Upsert Smile CDR users

See https://smilecdr.com/docs/json_admin_endpoints/user_management_endpoint.html
for more details on user management

Read JSON file with Smile CDR user objects
(see server/settings/users.example.json) and do following:

- Try creating user
- If user already exists, update user
"""

import argparse
import os
import json
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import secrets

from utils import send_request


def upsert(user_file, base_url, username=None, password=None, headers=None):
    """
    Upsert the smilecdr user payloads

    :param user_file: Path to JSON file with Smile CDR user objects
    :type user_file: str
    :param base_url: Smile CDR server base url
    :type base_url: str
    :param username: Username of user with permission to create/update users
    :type username: str
    :param password: Password of user with permission to create/update users
    :type password: str
    :param headers: Headers to send in HTTP request
    :type headers: str of the form key1=value1 key2=value2
    """
    print(f'Processing user file: {user_file} ...')

    with open(user_file, 'r') as user_json:
        users = json.load(user_json)

    submitted_users = []
    for user in users:
        print(f"Submitting user:{user['username']}")

        url = f'{base_url}/user-management/{user["nodeId"]}/{user["moduleId"]}'

        user.pop('pid', None)
        user['password'] = secrets.token_urlsafe(16)

        # Create headers dict
        header_dict = {}
        if headers:
            for kvpair in headers.split(' '):
                k, v = kvpair.split('=')
                header_dict[k.strip()] = v.strip()

        auth = None
        if username and password:
            header_dict.pop('Authorization', None)
            auth = HTTPBasicAuth(username, password)

        # Send POST request
        response = send_request(
            'post', url, auth=auth, json=user, headers=header_dict
        )
        resp_content = response_content(response)

        # User exists, send PUT request
        if response.status_code == 400 and (
            'already exists' in response.text or
            'manually create system users' in response.text
        ):
            print(
                f'User {user["username"]} already exists, '
                'try updating user ...'
            )
            # Get user's pid
            response = send_request(
                'get', f'{url}?searchTerm={user["username"]}',
                auth=auth, json=user, headers=header_dict
            )
            if response.status_code != 200:
                raise Exception(
                    f'Failed to update user {user["username"]}!'
                )
            # Update user
            pid = response_content(response)['users'][0]['pid']
            user.pop('password', None)
            response = send_request(
                'put', os.path.join(url, str(pid)),
                auth=auth, json=user, headers=header_dict
            )
            resp_content = response_content(response)

        if response.status_code not in {200, 201}:
            raise Exception(
                f'Failed to create or update user {user["username"]}!'
            )
        else:
            resp_content['password'] = user.get('password')
            submitted_users.append(resp_content)

    with open(user_file, 'w') as user_json:
        json.dump(submitted_users, user_json, indent=2, sort_keys=True)


def response_content(response):
    """
    Get response content. Try decoding as JSON first, otherwise return str
    version of content
    """
    try:
        resp_content = response.json()
    except json.decoder.JSONDecodeError:
        resp_content = response.text

    return resp_content


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'user_file', help='Path to a JSON file containing user '
        'payloads expected by smilecdr /user-management endpoint'
    )
    parser.add_argument(
        '--base_url', default='http://localhost:9000',
        help='URL of the FHIR server admin endpoint'
    )
    parser.add_argument(
        '--env_file',
        help='Path to an env file with username (DB_USERNAME) password '
        '(DB_PASSWORD) variables needed to create/update users. '
        'If this is not supplied then search for ``.env` in current working '
        'directory. If no env file is found, then variables will be sourced '
        'from environment.'
    )
    parser.add_argument(
        '--headers',
        help='The headers to add to HTTP requests. '
        'Format: header1=value header2=value'
    )
    args = parser.parse_args()

    env_file = args.env_file
    if not env_file:
        env_file = os.path.join(os.getcwd(), '.env')
    if os.path.isfile(env_file):
        load_dotenv(dotenv_path=env_file)

    upsert(
        args.user_file,
        username=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'),
        base_url=args.base_url,
        headers=args.headers
    )
