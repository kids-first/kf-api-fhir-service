import os
import json
from urllib.parse import urlparse
from pprint import pprint

from flask import Flask, request, jsonify, abort
import requests

import auth

app = Flask(__name__)


@app.post('/keycloak-proxy/<keycloak_endpoint>')
def auth_sandbox(keycloak_endpoint):
    """
    Test auth stuff out with keycloak
    """
    if keycloak_endpoint == "token":
        kwargs = request.get_json()
        if request.args.get("issuer"):
            kwargs.update({
                "issuer": request.args.get("issuer")
            })
        token = auth.get_access_token(**kwargs)
        return jsonify(token)
    else:
        abort(404)


if __name__ == "__main__":
    app.run(
        host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT"), debug=True
    )
