import os

from flask_appbuilder.security.manager import AUTH_OAUTH


# AUTH_TYPE = AUTH_OAUTH
# AUTH_USER_REGISTRATION = True
# AUTH_USER_REGISTRATION_ROLE = "Public"

# OAUTH_PROVIDERS = [{
#     'name': 'google',
#     # 'whitelist': ['@company.com'],
#     'icon': 'fa-google',
#     'token_key': 'access_token',
#     'remote_app': {
#         'client_id': 'GOOGLE_KEY',
#         'client_secret': 'GOOGLE_SECRET',
#         'api_base_url': 'https://www.googleapis.com/oauth2/v2/',
#         'client_kwargs':{ 'scope': 'openid email profile' },
#         'request_token_url': None,
#         'access_token_url': 'https://accounts.google.com/o/oauth2/token',
#         'authorize_url': 'https://accounts.google.com/o/oauth2/auth'
#     }
# }]

SECRET_KEY = os.getenv("SECRET_KEY")
SQLALCHEMY_DATABASE_URI=os.getenv("CONNECTION_STRING")
