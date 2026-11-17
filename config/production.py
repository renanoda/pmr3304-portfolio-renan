import os
from .settings import *

import dj_database_url

DEBUG = False
SECRET_KEY = os.environ["SECRET_KEY"]
hostname = os.environ["RENDER_EXTERNAL_HOSTNAME"]
ALLOWED_HOSTS = [hostname]
CSRF_TRUSTED_ORIGINS = [f"https://{hostname}"]
DATABASES = {"default": dj_database_url.parse(os.environ["DATABASE_URL"])}
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"
MIDDLEWARE = MIDDLEWARE.copy()
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
