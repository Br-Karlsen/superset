import os

from flask_appbuilder.security.manager import AUTH_OAUTH

ENABLE_PROXY_FIX = True
ROW_LIMIT = 5000
SECRET_KEY = os.getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = os.getenv("CONNECTION_STRING")
WTF_CSRF_ENABLED = False
CSRF_ENABLED = True
TALISMAN_ENABLED = False

## App icon
APP_NAME = "Br Karlsen Superset"
## APP_ICON = "https://storage.googleapis.com/databeat_website/airbyte-uploads/BrK-logo-Black.png"
APP_ICON_WIDTH = 200
## FAVICONS = [{"href": "https://yourdomain.com/favicon.png"}]


FEATURE_FLAGS = {
    "DASHBOARD_CROSS_FILTERS": True,
    "DRILL_TO_DETAIL": True,
    "GENERIC_X_AXES": True,
    "DASHBOARD_RBAC": True,
    "TAGGING_SYSTEM": True,
}

FILTER_STATE_CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_filter',
    'CACHE_REDIS_URL': os.getenv("SUPERSET_REDIS_CONNSTR"),
    'CACHE_REDIS_PASSWORD': os.getenv("SUPERSET_REDIS_PWD"),
}

EXPLORE_FORM_DATA_CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_explore',
    'CACHE_REDIS_URL': os.getenv("SUPERSET_REDIS_CONNSTR"),
    'CACHE_REDIS_PASSWORD': os.getenv("SUPERSET_REDIS_PWD"),
}
DATA_CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_data',
    'CACHE_REDIS_URL': os.getenv("SUPERSET_REDIS_CONNSTR"),
    'CACHE_REDIS_PASSWORD': os.getenv("SUPERSET_REDIS_PWD"),
}

CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,
    'CACHE_KEY_PREFIX': 'superset_meta',
    'CACHE_REDIS_URL': os.getenv("SUPERSET_REDIS_CONNSTR"),
    'CACHE_REDIS_PASSWORD': os.getenv("SUPERSET_REDIS_PWD"),
}


AUTH_TYPE = AUTH_OAUTH
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Gamma"

AUTH_ROLES_SYNC_AT_LOGIN = True

#Allow API to accept local db users
AUTH_API_LOGIN_ALLOW_MULTIPLE_PROVIDERS = True

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
    "an-brk-fin": ["brk-fin"],
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
