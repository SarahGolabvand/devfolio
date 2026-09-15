import dj_database_url
from .base import *
import os

DEBUG = True
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
]

DATABASES = {
    "default": dj_database_url.config(
        default=(
            f"postgres://"
            f"{config('DB_USER', default='postgres')}:"
            f"{config('DB_PASSWORD', default='postgres')}"
            f"@{config('DB_HOST', default='db')}:"
            f"{config('DB_PORT', default='5432')}/"
            f"{config('DB_NAME', default='portfolio_db')}"
        ),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

