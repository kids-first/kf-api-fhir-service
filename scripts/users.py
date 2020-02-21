import argparse
import os
import json
from pprint import pprint

import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
ENV_FILE = os.path.join(ROOT_DIR, 'smilecdr', '.env')
load_dotenv(dotenv_path=ENV_FILE)

BASE_URL = os.environ.get('FHIR_BASE_URL')
ENDPOINT = os.path.join(os.environ.get('FHIR_BASE_URL'), 'user-management')
ADMIN_USER = os.getenv('DB_CDR_USERID')
ADMIN_PW = os.getenv('DB_CDR_PASSWORD')


def create_or_update(user_file, update=False):
    """
    Create or update the smilecdr user payloads in the JSON file, `user_file`
    """
    print(f'Processing user file: {user_file} ...')
    with open(user_file, 'r') as user_json:
        users = json.load(user_json)['users']

    method_name = 'put' if update else 'post'
    auth = HTTPBasicAuth(ADMIN_USER, ADMIN_PW)
    for user in users:
        request_method = getattr(requests, method_name)
        url = f'{ENDPOINT}/{user["nodeId"]}/{user["moduleId"]}'

        if method_name == 'put':
            url = os.path.join(url, str(user.get('pid')))
        else:
            user.pop('id', None)

        print(f'{method_name.upper()} {url}')
        response = request_method(url, auth=auth, json=user)

        try:
            resp_content = response.json()
        except json.decoder.JSONDecodeError:
            resp_content = response.text

        pprint(resp_content)

        if response.status_code in [200, 201]:
            print(f'✅ Request succeeded, status: {response.status_code}')
            user['pid'] = resp_content.get('pid')
        else:
            print(f'❌ Request failed, status: {response.status_code}')

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
