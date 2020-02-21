import argparse
import os
from collections import defaultdict

from utils import properties_to_dict, send_request
from pprint import pprint

from config import BASE_URL

ENDPOINT = os.path.join(BASE_URL, 'module-config')
DEFAULT_PREFIXES = {'module.clustermgr', 'node'}


def properties_to_module_config_dict(properties_dict):
    module_dict = defaultdict(dict)
    for k, v in properties_dict.items():
        if not valid(k, skip=DEFAULT_PREFIXES):
            continue

        parts = k.split('.')
        module_id = parts[1]
        module_dict[module_id].update({'moduleId': module_id})

        if parts[-1] == 'type':
            module_dict[module_id].update({'moduleType': v})
        elif parts[2] == 'config':
            if 'options' not in module_dict[module_id]:
                module_dict[module_id]['options'] = []
            options = module_dict[module_id]['options']
            options.append({'key': k.split('config.')[-1], 'value': v})
            module_dict[module_id]['options'] = options

    return module_dict


def valid(key, skip=DEFAULT_PREFIXES):
    for p in skip:
        if key.startswith(p):
            return False
    return True


def load(properties_file, skip=DEFAULT_PREFIXES):
    props = properties_to_dict(properties_file)
    module_dict = properties_to_module_config_dict(props)

    for module_id, config in module_dict.items():
        url = os.path.join(
            ENDPOINT, 'Master', module_id
        )
        response = send_request('get', url)
        config.update(response.json())
        pprint(config)
        url = os.path.join(url, 'set')
        response = send_request('put', url, json=config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'properties_file', help='Path to server properties file'
    )
    args = parser.parse_args()
    load(args.properties_file)
