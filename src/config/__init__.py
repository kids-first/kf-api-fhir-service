import os

from dotenv import find_dotenv, load_dotenv

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname((__file__))))
DATA_DIR = os.path.join(ROOT_DIR, "data", "resources")
SEED_USERS_FILEPATH = os.path.join(ROOT_DIR, "smilecdr/settings", "users.json")

DOTENV_PATH = find_dotenv()
if DOTENV_PATH:
    load_dotenv(DOTENV_PATH)

BASE_URL = os.environ.get("FHIR_ENDPOINT")
FHIR_URL = BASE_URL
USER_MGMNT_ENDPOINT = os.environ.get("USER_MGMNT_ENDPOINT")
KEYCLOAK_PROXY_URL = os.environ.get(
    "KEYCLOAK_PROXY_URL", "http://localhost:8081/keycloak-proxy"
)
KEYCLOAK_CLIENT_ID = os.environ.get("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = os.environ.get("KEYCLOAK_CLIENT_SECRET")
KEYCLOAK_ISSUER = os.environ.get("KEYCLOAK_ISSUER")
