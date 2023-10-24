import os

from flask_appbuilder.security.manager import AUTH_OAUTH

ENABLE_PROXY_FIX = True
ROW_LIMIT = 5000
SECRET_KEY = os.getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = os.getenv("CONNECTION_STRING")
WTF_CSRF_ENABLED = True
CSRF_ENABLED = True

FEATURE_FLAGS = {
    "DASHBOARD_CROSS_FILTERS": True,
    "DRILL_TO_DETAIL": True,
    "GENERIC_X_AXES": True,
    "DASHBOARD_RBAC": True,
    "TAGGING_SYSTEM": True,
    
}


AUTH_TYPE = AUTH_OAUTH
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Gamma"

AUTH_ROLES_SYNC_AT_LOGIN = True

# A mapping from LDAP/OAUTH group names to FAB roles
AUTH_ROLES_MAPPING = {
    "an-brk": ["brk"],
    "an-admin": ["Admin"],
    "an-brk-hr": ["brk-hr"],
    "an-akv": ["akv"],
    "an-flk": ["flk"],
    "an-akv-hr": ["akv-hr"],
    "an-flk-hr": ["flk-hr"],
    "an-konsern": ["konsern-hr"],
    "an-stingray": ["stingray"],
    "an-salaks": ["salaks"],
}

OAUTH_PROVIDERS = [
    {
        "name": "azure",
        "icon": "fa-windows",
        "token_key": "access_token",
        "remote_app": {
            "client_id": os.getenv("AZURE_ID"),
            "client_secret": os.getenv("AZURE_SECRET"),
            "api_base_url": "https://login.microsoftonline.com/"
            + os.getenv("TENANT_ID")
            + "/oauth2",
            "client_kwargs": {
                "scope": "User.read name preferred_username email profile upn groups",
                "resource": os.getenv("AZURE_ID"),
            },
            "request_token_url": None,
            "access_token_url": "https://login.microsoftonline.com/"
            + os.getenv("TENANT_ID")
            + "/oauth2/token",
            "authorize_url": "https://login.microsoftonline.com/"
            + os.getenv("TENANT_ID")
            + "/oauth2/authorize",
        },
    }
]
