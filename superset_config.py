import os

SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY")

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/superset'
