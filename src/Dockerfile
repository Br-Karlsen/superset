FROM apache/superset:3.0.0

COPY superset_config.py /etc/superset/superset_config.py
COPY requirements-local.txt ./docker/requirements-local.txt

# Switching to root to install the required packages
USER root

# install postgres, bigquery driver and oauth
RUN pip install psycopg2-binary sqlalchemy-bigquery Authlib

# Switching back to using the `superset` user
USER superset
ENV SUPERSET_CONFIG_PATH=/etc/superset/superset_config.py