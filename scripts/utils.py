"""
Helpers
"""
import json
from pprint import pprint

import requests
from requests.auth import HTTPBasicAuth

from config import ADMIN_USER, ADMIN_PW


def send_request(method_name, url, **request_kwargs):
    """
    Send an HTTP request
    """
    print(f'{method_name.upper()} {url}')
    request_method = getattr(requests, method_name.lower())
    if 'auth' not in request_kwargs:
        request_kwargs['auth'] = HTTPBasicAuth(ADMIN_USER, ADMIN_PW)
    response = request_method(url, **request_kwargs)

    try:
        resp_content = response.json()
    except json.decoder.JSONDecodeError:
        resp_content = response.text

    pprint(resp_content)

    if response.status_code in [200, 201]:
        print(
            f'✅ {method_name.upper()} request succeeded, '
            f'status: {response.status_code}')
    else:
        print(
            f'❌ {method_name.upper()} request failed, status: '
            f'{response.status_code}')

    return response


def properties_to_dict(filepath):
    """
    Convert Java .properties file to a dict

    Only include non-commented lines
    """
    out = {}
    with open(filepath) as prop_file:
        for line in prop_file.readlines():
            line = line.strip()
            if line and (not line.startswith('#')):
                k, v = line.split('=')
                out[k.strip()] = v.strip()
    return out


def dict_to_properties(data, filepath, delim='='):
    """
    Convert a dict to a Java .properties file
    """
    prop_strings = [
        f'{k}={v}'
        for k, v in data.items()
    ]
    with open(filepath, 'w') as prop_file:
        prop_file.write('\n'.join(prop_strings))
