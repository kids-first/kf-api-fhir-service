"""
Update the smilecdr server settings with the settings in the
smilecdr Java .properties file

Restart the server's module-configs after the updates are complete.
"""

import argparse
import os
from collections import defaultdict
from copy import deepcopy

from utils import properties_to_dict, send_request
from pprint import pprint, pformat

from config import BASE_URL

ENDPOINT = os.path.join(BASE_URL, 'module-config')
DEFAULT_SKIP_PREFIXES = {'module.clustermgr', 'node'}
MODULE_IDS = {
    'persistence',
    'local_security',
    'fhir_endpoint',
    'fhirweb_endpoint',
    'admin_json',
    'admin_web',
    'smart_auth',
    'subscription'
}


def load(properties_file, module_ids=None, restart_modules=False):
    """
    Update the smilecdr server settings with the settings in the
    smilecdr Java .property file `properties_file`.

    Only update module-configs whose ids are in `module-ids`
    Skip properties that start with any of the DEFAULT_SKIP_PREFIXES

    Sends PUT requests to /module-config/Master/<module-config id>/set
    """

    # Convert smilecdr properties to module-config dicts expected by server
    props = properties_to_dict(properties_file)
    module_config = properties_to_module_config_dict(props)

    # ----- Update server settings with new module-configs -----
    if module_ids:
        module_ids = set(module_ids.split(','))

    for module_id, config in module_config.items():
        if module_ids and (module_id not in module_ids):
            print(f'Skipping module-config {module_id}')
            continue

        base_url = os.path.join(
            ENDPOINT, 'Master', module_id
        )
        # Get current module config
        response = send_request('get', base_url)

        # Manual patch of module config
        config = merge_module_config_opts(config, response.json())
        print(f'Manually patched module-config looks like:\n{pformat(config)}')

        # Replace with patched module config
        url = os.path.join(base_url, 'set')
        response = send_request('put', url, json=config)

        if restart_modules:
            # Initiate restart module
            if response.status_code in {200, 201}:
                print(f'Restarting module {module_id} ...')
                url = os.path.join(base_url, 'restart')
                response = send_request('post', url)


def merge_module_config_opts(curr, new):
    """
    Merge two options lists from two smilecdr module-configs payloads

    An options list looks like [{"key": <property>, "value": <value>}, ...]
    Convert both options lists from curr and new to dicts
    Update the current options dict with the new options dict
    Convert the current options dict back to an options list
    """
    out = deepcopy(curr)

    def opt_list_to_dict(options):
        return {
            opt['key']: opt['value']
            for opt in options
        }
    # Convert opts list to dict
    curr_options = opt_list_to_dict(curr.get('options'))
    # Merge new opts into current opts dict
    curr_options.update(opt_list_to_dict(new.get('options')))
    # Update the module-config with new options list
    out['options'] = [
        {'key': k, 'value': v}
        for k, v in curr_options.items()
    ]
    # Merge in the other keys from new
    for k, v in new.items():
        if k not in out:
            out[k] = v
    return out


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
        if k.startswith(tuple(DEFAULT_SKIP_PREFIXES)):
            continue

        parts = k.split('.')
        module_id = parts[1]
        module_config[module_id].update({'moduleId': module_id})

        # Property strings with .type and .requires are not real properties
        # All other strings are
        if parts[2] not in {'type', 'requires'}:
            # Init options list
            if 'options' not in module_config[module_id]:
                module_config[module_id]['options'] = []
            options = module_config[module_id]['options']
            options.append({'key': k.split(parts[2] + '.')[-1], 'value': v})
            module_config[module_id]['options'] = options

    return module_config


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'properties_file', help='Path to smilecdr Java properties file'
    )
    parser.add_argument(
        '--module_ids',
        help='Comma delimited string listing ids for the smilecdr '
        'module-configs you want to update. If this option is not included '
        'then all module-configs will be updated. the module-config ids are: '
        f'{pformat(MODULE_IDS)}'
    )
    parser.add_argument(
        '--restart_modules', action='store_true',
        help='Whether or not to restart the modules after the setttings '
        'updates have been sent to the server'
    )
    args = parser.parse_args()
    load(
        args.properties_file,
        module_ids=args.module_ids,
        restart_modules=args.restart_modules
    )
