FROM apache/superset:2.0.1

#COPY superset_config.py /etc/superset/superset_config.py
COPY superset_config.py /etc/superset/superset_config.py
COPY requirements-local.txt ./docker/requirements-local.txt

# Switching to root to install the required packages
USER root

# install postgres and bigquery driver
#RUN pip install psycopg2-binary pandas-gbq pybigquery
RUN pip install psycopg2-binary sqlalchemy-bigquery Authlib

# Switching back to using the `superset` user
USER superset
ENV SUPERSET_CONFIG_PATH=/etc/superset/superset_config.py