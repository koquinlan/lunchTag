from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "lunch_tag_local",
        "USER": "postgres",
        "PASSWORD": get_env_variable("POSTGRES_PW"),
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}
