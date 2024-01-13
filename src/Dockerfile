FROM apache/superset:3.0.1

COPY superset_config.py /etc/superset/superset_config.py
COPY requirements-local.txt ./docker/requirements-local.txt
COPY brk-logo.png  /app/superset/static/assets/images/superset-logo-horiz.png

# Switching to root to install the required packages
USER root

# install postgres, bigquery driver and oauth
RUN pip install psycopg2-binary sqlalchemy-bigquery Authlib "Cython>=0.22" NumPy 
#RUN pip install -v --only-binary lunarcalendar tqdm "pystan<3.0" && pip install "prophet>=1.0.1, <1.1"
RUN pip install -v --only-binary lunarcalendar tqdm pystan prophet
# Switching back to using the `superset` user
USER superset
ENV SUPERSET_CONFIG_PATH=/etc/superset/superset_config.py