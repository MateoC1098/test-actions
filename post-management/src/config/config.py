import os
import sys
from dotenv import load_dotenv

load_dotenv()
DB_USER = os.getenv("DB_USER") or 'postgres'
DB_PASSWORD = os.getenv("DB_PASSWORD") or 'postgres'
DB_HOST = os.getenv("DB_HOST") or 'localhost'
DB_PORT = os.getenv("DB_PORT") or '5432'
DB_NAME = os.getenv("DB_NAME") or 'post_management'
USERS_PATH = os.getenv("USERS_PATH")

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = False