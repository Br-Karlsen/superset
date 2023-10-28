<<<<<<< HEAD
FROM apache/superset:3.0.0
=======
FROM apache/superset:2.1.0
>>>>>>> b62226bcad07281687f733929204daae6a162dcd

COPY superset_config.py /etc/superset/superset_config.py
COPY requirements-local.txt ./docker/requirements-local.txt

# Switching to root to install the required packages
USER root

# install postgres, bigquery driver and oauth
RUN pip install psycopg2-binary sqlalchemy-bigquery Authlib

# Switching back to using the `superset` user
USER superset
ENV SUPERSET_CONFIG_PATH=/etc/superset/superset_config.py