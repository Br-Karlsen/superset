FROM apache/superset

ENV PYTHONPATH="/app"

WORKDIR /app
COPY superset_config.py /app/superset_config.py

# Switching to root to install the required packages
USER root

# install Postgres driver to connect to metadata database
RUN pip install psycopg2-binary pandas-gbq pybigquery

# Switching back to using the `superset` user
USER superset
