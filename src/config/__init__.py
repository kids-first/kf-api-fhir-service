import os

from dotenv import find_dotenv, load_dotenv

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname((__file__))))
DATA_DIR = os.path.join(ROOT_DIR, "data", "resources")
SEED_USERS_FILEPATH = os.path.join(ROOT_DIR, "smilecdr/settings", "users.json")
SEARCH_PARAMETER_DIR = os.path.join(ROOT_DIR, "smilecdr/search_parameters")

DOTENV_PATH = find_dotenv()
if DOTENV_PATH:
    load_dotenv(DOTENV_PATH)

BASE_URL = os.environ.get("FHIR_ENDPOINT")
FHIR_URL = BASE_URL
FHIR_DIRECT_URL = os.environ.get("FHIR_DIRECT_ENDPOINT")
FHIR_APP_ADMIN = os.environ.get("FHIR_APP_ADMIN")
FHIR_APP_ADMIN_PW = os.environ.get("FHIR_APP_ADMIN_PW")
FHIR_TEST_USER_PW = os.environ.get("FHIR_TEST_USER_PW")
USER_MGMNT_ENDPOINT = os.environ.get("USER_MGMNT_ENDPOINT")
REINDEX_ENDPOINT = os.environ.get("REINDEX_ENDPOINT")
KEYCLOAK_PROXY_URL = os.environ.get(
    "KEYCLOAK_PROXY_URL", "http://localhost:8081/keycloak-proxy"
)
KEYCLOAK_CLIENT_ID = os.environ.get("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = os.environ.get("KEYCLOAK_CLIENT_SECRET")
KEYCLOAK_READ_CLIENT_ID = os.environ.get("KEYCLOAK_READ_CLIENT_ID")
KEYCLOAK_READ_CLIENT_SECRET = os.environ.get("KEYCLOAK_READ_CLIENT_SECRET")
KEYCLOAK_ISSUER = os.environ.get("KEYCLOAK_ISSUER")

REINDEX_PAYLOAD= {
  "resourceType": "Parameters",
  "parameter": [ {
    "name": "url",
    "valueString": "Patient?"
  }]
}
