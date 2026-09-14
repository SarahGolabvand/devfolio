import dj_database_url
from .base import *

DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',') if s.strip()])


DATABASES = {
    'default': dj_database_url.config(
        default=f"postgres://{config('DB_USER', default='postgres')}:{config('DB_PASSWORD', default='postgres_pass')}@{config('DB_HOST', default='db')}:{config('DB_PORT', default='5432')}/{config('DB_NAME', default='portfolio_db')}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

MIDDLEWARE = list(MIDDLEWARE)
if "whitenoise.middleware.WhiteNoiseMiddleware" not in MIDDLEWARE:
    try:
        sec_index = MIDDLEWARE.index("django.middleware.security.SecurityMiddleware")
        MIDDLEWARE.insert(sec_index + 1, "whitenoise.middleware.WhiteNoiseMiddleware")
    except ValueError:
        MIDDLEWARE.insert(0, "whitenoise.middleware.WhiteNoiseMiddleware")


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
