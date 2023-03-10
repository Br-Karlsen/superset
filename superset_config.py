import os

from flask_appbuilder.security.manager import AUTH_OAUTH

SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY")
SQLALCHEMY_DATABASE_URI=os.getenv("SUPERSET_CONNECTION_STRING")

AUTH_TYPE = AUTH_OAUTH
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Gamma"

AUTH_ROLES_SYNC_AT_LOGIN = True

# A mapping from LDAP/OAUTH group names to FAB roles
AUTH_ROLES_MAPPING = {
    "an-brk": ["brk"],
    # "ADMIN_GROUP_NAME": ["Admin"],

}

OAUTH_PROVIDERS = [
    {
        "name": "azure",
        # "whitelist": ["@company.com"],
        "icon": "fa-windows",
        "token_key": "access_token",
        "remote_app": {
            "client_id": os.getenv("AZURE_ID"),
            "client_secret": os.getenv("AZURE_SECRET"),
            "api_base_url": "https://login.microsoftonline.com/886f0b1c-59ba-405b-ba4a-0147eaa429c0/oauth2",
            "client_kwargs": {
                "scope": "User.read name preferred_username email profile upn groups",
                "resource": os.getenv("AZURE_ID"),
            },
            "request_token_url": None,
            "access_token_url": "https://login.microsoftonline.com/886f0b1c-59ba-405b-ba4a-0147eaa429c0/oauth2/token",
            "authorize_url": "https://login.microsoftonline.com/886f0b1c-59ba-405b-ba4a-0147eaa429c0/oauth2/authorize",
        },
    }
]