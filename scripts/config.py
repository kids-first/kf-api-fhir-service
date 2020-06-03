import os

from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
ENV_FILE = os.path.join(ROOT_DIR, 'smilecdr', '.env')
load_dotenv(dotenv_path=ENV_FILE)

BASE_URL = os.environ.get('FHIR_BASE_URL')
ADMIN_USER = os.getenv('DB_USERNAME')
ADMIN_PW = os.getenv('DB_PASSWORD')
