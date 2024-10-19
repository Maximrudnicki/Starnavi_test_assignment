from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get("API_KEY")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS")
SECRET_KEY = os.environ.get("SECRET_KEY")
