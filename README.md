# Apache Superset on Google Cloud Run
This repository is designed to be opened on a machine with [Docker](https://www.docker.com/) installed. When opened in [Visual Studio Code](https://code.visualstudio.com/) with the [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension installed, Visual Studio Code can open the repository in its own container using all Python requirements specified in this repository's `requirements.txt` file.


## Metadata database
Before you deploy Superset to Cloud Run, you need to see a metadata database. The below steps assume you already have a PostgreSQL Cloud SQL instance created.

```bash

gcloud auth login;
gcloud config set project <GOOGLE_CLOUD_PROJECT_ID>;

gcloud services enable artifactregistry.googleapis.com;
gcloud services enable cloudbuild.googleapis.com;
gcloud services enable run.googleapis.com;

gcloud iam service-accounts create superset;

# create secrets
# superset-connection-string: postgresql+psycopg2://username:password@/dbname?host=/cloudsql/CLOUD-SQL-CONNECTION-NAME
# superset-secret-key

gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="serviceAccount:superset@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com" \
    --role=roles/cloudsql.client;

gcloud beta secrets add-iam-policy-binding projects/$GOOGLE_CLOUD_PROJECT/secrets/superset-connection-string \
    --member serviceAccount:superset@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor;

gcloud beta secrets add-iam-policy-binding projects/$GOOGLE_CLOUD_PROJECT/secrets/superset-secret-key \
    --member serviceAccount:superset@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor;

# create database for superset metadata
gcloud sql databases create 'superset' --instance=<CLOUD_SQL_INSTANCE_NAME>;

# connect to cloud sql instance via cloud sql proxy
# keep proxy running while executing the next command
/cloud_sql_proxy -instances=<INSTANCE_CONNECTION_NAME>=tcp:5432;

# initialize superset database
superset db upgrade;

# create admin user in db
superset fab create-admin;

# create roles and grant permissions
superset init;

```

## Cloud Run

```bash

# create artifact registry repository
gcloud artifacts repositories create my-repository \
    --project=$GOOGLE_CLOUD_PROJECT \
    --repository-format=docker \
    --location=us-central1 \
    --description="Docker repository";

gcloud builds submit \
    --tag us-central1-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/my-repository/superset src/.;


gcloud beta run deploy superset \
    --image=us-central1-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/my-repository/superset \
    --allow-unauthenticated \
    --port=8088 \
    --cpu=2 \
    --memory=4096Mi \
    --min-instances=1 \
    --max-instances=1 \
    --set-secrets=CONNECTION_STRING=superset-connection-string:1,SECRET_KEY=superset-secret-key:1 \
    --set-cloudsql-instances <INSTANCE_CONNECTION_NAME> \
    --platform=managed \
    --service-account superset@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com \
    --region=us-central1;

```

<!-- ## Enabling Google Auth
In a Google Cloud project:

1. Head to APIs & Services > OAuth consent screen
2. Select *Internal* and click **Create**
3.  -->
