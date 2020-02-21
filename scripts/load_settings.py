"""
Update the smilecdr server settings with the settings in the
smilecdr Java .properties file

Restart the server's module-configs after the updates are complete.
"""

import argparse
import os
from collections import defaultdict

from utils import properties_to_dict, send_request
from pprint import pprint

from config import BASE_URL

ENDPOINT = os.path.join(BASE_URL, 'module-config')
DEFAULT_SKIP_PREFIXES = {'module.clustermgr', 'node'}


def properties_to_module_config_dict(properties_dict):
    """
    Convert the smilecdr Java .properties file into smilecdr `module-config`
    dicts

    See https://smilecdr.com/docs/json_admin_endpoints/module_config_endpoint.html#fetch-config-single-module
    for details
    """
    module_config = defaultdict(dict)
    for k, v in properties_dict.items():
        # Skip properties we don't want to update
        if not k.startswith(tuple(DEFAULT_SKIP_PREFIXES)):
            continue

        parts = k.split('.')
        module_id = parts[1]
        module_config[module_id].update({'moduleId': module_id})

        # Property strings with .config are ones we wan't to update
        # Anything else isn't a real property in the module config
        if parts[2] == 'config':
            if 'options' not in module_config[module_id]:
                module_config[module_id]['options'] = []
            options = module_config[module_id]['options']
            options.append({'key': k.split('config.')[-1], 'value': v})
            module_config[module_id]['options'] = options

    return module_config


def load(properties_file, skip=DEFAULT_SKIP_PREFIXES):
    """
    Update the smilecdr server settings with the settings in the
    smilecdr Java .property file `properties_file`.

    Skip properties that start with any of the DEFAULT_SKIP_PREFIXES

    Sends PUT requests to /module-config/Master/<module-config id>/set
    """

    # Convert smilecdr properties to module-config dicts expected by server
    props = properties_to_dict(properties_file)
    module_config = properties_to_module_config_dict(props)

    # Update server settings with new module-configs
    # Restart each module after update is complete
    for module_id, config in module_config.items():
        url = os.path.join(
            ENDPOINT, 'Master', module_id
        )
        response = send_request('get', url)
        config.update(response.json())
        pprint(config)
        url = os.path.join(url, 'set')
        response = send_request('put', url, json=config)

        if response.status_code in {200, 201}:
            response = send_request('put', url, json=config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'properties_file', help='Path to smilecdr Java properties file'
    )
    args = parser.parse_args()
    load(args.properties_file)
