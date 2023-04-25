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
