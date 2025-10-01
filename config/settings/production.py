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

# Production email configuration for Heroku + SendGrid
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'  # SendGrid uses 'apikey' as username
EMAIL_HOST_PASSWORD = get_env_variable("SENDGRID_API_KEY")  # Set by Heroku SendGrid addon

# Alternative: If you want to use Gmail instead of SendGrid
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = get_env_variable("GMAIL_USER")  # Your Gmail address
# EMAIL_HOST_PASSWORD = get_env_variable("GMAIL_APP_PASSWORD")  # Gmail app password
