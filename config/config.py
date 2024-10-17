from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_DB = os.environ.get("MONGODB_DB")
MONGODB_STRING = os.environ.get("MONGODB_STRING")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS")
SECRET_KEY = os.environ.get("SECRET_KEY")
