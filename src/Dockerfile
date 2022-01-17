FROM apache/superset:71e3fa1bf350045da9a1c1e89443549c204a3516

# ENV PYTHONPATH "${PYTHONPATH}:/app/pythonpath"
COPY superset_config.py /app/pythonpath/superset_config.py

# Switching to root to install the required packages
USER root

# install Postgres driver to connect to metadata database
RUN pip install psycopg2-binary pandas-gbq pybigquery

# Switching back to using the `superset` user
USER superset
