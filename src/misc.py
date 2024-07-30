"""
Miscellaneous utility functions
"""
import time
import json
from pprint import pformat

import requests


def elapsed_time_hms(start_time):
    """
    Get time elapsed since start_time in hh:mm:ss str format
    """
    elapsed = time.time() - start_time
    return time.strftime('%H:%M:%S', time.gmtime(elapsed))


def send_request(method, *args, ignore_status_codes=None, **kwargs):
    """Send http request. Raise exception on status_code >= 300

    :param method: name of the requests method to call
    :type method: str
    :raises: requests.Exception.HTTPError
    :returns: requests Response object
    :rtype: requests.Response
    """
    if isinstance(ignore_status_codes, str):
        ignore_status_codes = [ignore_status_codes]

    # NOTE: Set timeout so requests don't hang
    # See https://requests.readthedocs.io/en/latest/user/advanced/#timeouts
    if not kwargs.get("timeout"):
        # connect timeout, read timeout
        kwargs["timeout"] = (3, 60)
    else:
        print(
            f"⌚️ Applying user timeout: {kwargs['timeout']} (connect, read)"
            " seconds to request"
        )

    requests_op = getattr(requests, method.lower())
    status_code = 0
    try:
        resp = requests_op(*args, **kwargs)
        status_code = resp.status_code
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if ignore_status_codes and (status_code in ignore_status_codes):
            pass
        else:
            body = ""
            try:
                body = pformat(resp.json())
            except:
                body = resp.text

            msg = (
                f"❌ Problem sending {method} request to server\n"
                f"{str(e)}\n"
                f"args: {args}\n"
                f"kwargs: {pformat(kwargs)}\n"
                f"{body}\n"
            )
            print(msg)
            raise e

    return resp


def read_json(filepath, default=None):
    """
    Read JSON file into Python dict. If default is not None and the file
    does not exist, then return default.

    :param filepath: path to JSON file
    :type filepath: str
    :param default: default return value if file not found, defaults to None
    :type default: any, optional
    :returns: your data
    :rtype: dict
    """
    if (default is not None) and (not os.path.isfile(filepath)):
        return default

    with open(filepath, "r") as json_file:
        return json.load(json_file)
