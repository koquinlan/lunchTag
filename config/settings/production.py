from .base import *
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", ".herokuapp.com"]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "lunchtag",
        "USER": "name",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "",
    }
}

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # one month

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES["default"].update(db_from_env)

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": "hyyxwq1o9",
    "API_KEY": get_env_variable("API_KEY"),
    "API_SECRET": get_env_variable("API_SECRET"),
}
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
