# Apache Superset on Google Cloud Run
This repository deploys Apache Superset to Google Cloud Run and configures it to use Google for authentication. This is a piece of the larger K12 open source data stack shown below. This can be a powerful solution. When you have a visualization platform with row level security and no per-seat license, you have the ability to put data in front of all users: school leaders, staff, and students.

![K12 open source data stack](/assets/open-source-data-stack.png)

This repository is designed to be opened on a machine with [Docker](https://www.docker.com/) installed. When opened in [Visual Studio Code](https://code.visualstudio.com/) with the [Remote Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension installed, Visual Studio Code can open the repository in its own container using all Python requirements specified in this repository's `requirements.txt` file.

Prior to opening the repo in dev containers, copy `.env-sample` to create your own `.env` file.

The deployment process below can feel a little random and disjointed at times. This is due to needing to perform steps such as an initial Cloud Run deployment to receive a service URL to then go back and finish the configuration of a previous step. Trust the process and run through in the order detailed below.

## Configuring Google oAuth
This Superset deployment will use Google for authentication. The steps below will configure your Google Cloud project to allow your users to authenticate with Superset.

### Configure consent screen

1. Head to APIs & Services > OAuth consent screen
2. Select *Internal* and click **Create**
3. Set the following:
    * App name
    * User support email
    * Authorized domains
    * Developer contact information
4. Click **Save and continue**
5. Click **Add or Remove Scopes**
6. Select *email* and *profile* scopes and click **Update**
7. Click **Save and continue**

### Create credentials

1. Head to APIs & Services > Credentials
2. Click **Create credentials**, *OAuth Client ID*
3. Select **Application type**: *Web application*
4. Make note of the client id and client secret

## Secrets
Your Cloud Run service will pull secrets from Google's Secret Manager and mount them as environment variables in the containers. Navigate to [Secret Manager](https://console.cloud.google.com/security/secret-manager) under the *IAM & Admin* menu.

### Superset connection string
* Create a new secret with the name `superset-connection-string`
* Enter a valid connection string that Superset will use to connect to your metadata db
* Click **Create Secret**

*Cconnection string format:*
```bash
postgresql+psycopg2://postgres:<POSTGRES-PASSWORD>@/superset?host=/cloudsql/<INSTANCE_CONNECTION_NAME>
```

### Superset secret key

* Create a new secret with the name `superset-secret-key`
* Enter a really long string that Superset will use when encrypting things like database passwords
* Click **Create Secret**

### Google oAuth credentials
Create two secrets to store your Google oAuth client information.

* `google-client-id`
* `google-client-secret`


## Metadata database
Before you deploy Superset to Cloud Run, you need to seed a metadata database. This will be a PostgreSQL database that stores things such as your chart configurations, users, roles, and permissions. The below steps assume you already have a PostgreSQL Cloud SQL instance created.

```bash

gcloud auth login;
gcloud config set project $GOOGLE_CLOUD_PROJECT;

# enable necessary apis for the steps below
gcloud services enable artifactregistry.googleapis.com;
gcloud services enable cloudbuild.googleapis.com;
gcloud services enable run.googleapis.com;

# create service account that Cloud Run service will run under
gcloud iam service-accounts create superset;

# add various IAM roles to the service account
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="serviceAccount:superset@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com" \
    --role=roles/cloudsql.client;

gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="serviceAccount:superset@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com" \
    --role=roles/bigquery.jobUser;

gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="serviceAccount:superset@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com" \
    --role=roles/bigquery.dataViewer;

# give service account access to the secrets
gcloud beta secrets add-iam-policy-binding projects/$GOOGLE_CLOUD_PROJECT/secrets/superset-connection-string \
    --member serviceAccount:superset@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor;

gcloud beta secrets add-iam-policy-binding projects/$GOOGLE_CLOUD_PROJECT/secrets/superset-secret-key \
    --member serviceAccount:superset@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor;

gcloud beta secrets add-iam-policy-binding projects/$GOOGLE_CLOUD_PROJECT/secrets/google-client-id \
    --member serviceAccount:superset@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor;

gcloud beta secrets add-iam-policy-binding projects/$GOOGLE_CLOUD_PROJECT/secrets/google-client-secret \
    --member serviceAccount:superset@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com \
    --role roles/secretmanager.secretAccessor;

# create database for superset metadata
gcloud sql databases create 'superset' --instance=<CLOUD_SQL_INSTANCE_NAME>;

# connect to cloud sql instance via cloud sql proxy
# keep proxy running while executing the next command
/cloud_sql_proxy -instances=<INSTANCE_CONNECTION_NAME>=tcp:5432;

# initialize superset database
superset db upgrade;

```

## Cloud Run
The commands below will push a Docker image to a Google Artifact Registry within the Google Cloud project. A Cloud Run service will them be created to deploy that image.

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
    --min-instances=0 \
    --max-instances=1 \
    --set-secrets=CONNECTION_STRING=superset-connection-string:1,SECRET_KEY=superset-secret-key:1,GOOGLE_ID=google-client-id:1,GOOGLE_SECRET=google-client-secret:1 \
    --set-cloudsql-instances <INSTANCE_CONNECTION_NAME> \
    --platform=managed \
    --service-account superset@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com \
    --region=us-central1;

```

After running the `gcloud beta run` command above, you will recieve a Google Cloud Run service URL. Head back to APIs & Services > Credentials, edit your credential, and update the *Authorized redirect URI* to *`<CLOUD-RUN-URL>`/oauth-authorized/google*

Navigate to your Cloud Run service URL. This will authenticate you as an admin of the Superset deployment. Once you've done that, you will need to run the steps below to lock down the deployment.

## Refresh Superset roles
Update `AUTH_USER_REGISTRATION_ROLE` in `superset_config.py` to "Public". All new accounts moving forward will default to Public and no longer Admin. 

```bash

# create roles and grant permissions
superset init;

# push an updated image to artifact registry
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
    --set-secrets=CONNECTION_STRING=superset-connection-string:1,SECRET_KEY=superset-secret-key:1,GOOGLE_ID=google-client-id:1,GOOGLE_SECRET=google-client-secret:1 \
    --set-cloudsql-instances <INSTANCE_CONNECTION_NAME> \
    --platform=managed \
    --service-account superset@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com \
    --region=us-central1;


```
