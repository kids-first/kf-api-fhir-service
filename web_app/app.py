import os
import json
from urllib.parse import urlparse
from pprint import pprint

from flask import Flask, request, jsonify, abort
import requests

import auth

app = Flask(__name__)


@app.post('/token')
def auth_sandbox():
    """
    Test auth stuff out with keycloak
    """
    kwargs = request.get_json()
    if request.args.get("issuer"):
        kwargs.update({
            "issuer": request.args.get("issuer")
        })
    token = auth.get_access_token(**kwargs)

    return jsonify(token)


@app.post('/keycloak-proxy')
def keycloak():
    """
    Forward requests to keycloak whether it is internal inside docker network
    or in an externally resolvable network
    """
    payload = request.get_json()

    http_op = payload.pop("http_operation", "get")
    endpoint = payload.pop("endpoint", None)
    kwargs = payload.get("kwargs", None)

    resp = auth.send_request(http_op, endpoint, **kwargs)

    return jsonify(resp.json())


if __name__ == "__main__":
    app.run(
        host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT"), debug=True
    )
