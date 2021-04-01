"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from environs import Env
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    
    # 3rd parties
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'mptt',
    'channels',
    'debug_toolbar',
    
    
    # Locals
    'accounts',
    'boards',
    'chat',
]
INSTALLED_APPS += ('django_summernote', )

SUMMERNOTE_THEME = 'bs4'
CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# get ip in docker for debug toolbar.
import socket
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + '1' for ip in ips]
print(INTERNAL_IPS[0])

# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
# SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=2592000)
# SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
# SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
# SESSION_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE", default=True)
# CSRF_COOKIE_SECURE = env.bool("DJANGO_CSRF_COOKIE_SECURE", default=True)
# X_FRAME_OPTIONS = 'DENY'



ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR.joinpath('templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            # Set the hostname in docker-compose.yml file.
            "hosts": [("comm_redis", 6379)],
        },
    },
}
# container ip check
# docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' django

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/staticfiles/'
STATICFILES_DIRS = [
    str(BASE_DIR.joinpath('static')),
]
STATIC_ROOT = str(BASE_DIR.joinpath('staticfiles'))

MEDIA_URL = '/media/'
MEDIA_ROOT = str(BASE_DIR.joinpath('media/'))

AUTH_USER_MODEL = 'accounts.CustomUser'

# allauth
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]
 # Since allauth sends verification Email to new user, email backends needs to be set.
 # For dev, ACCOUNT_EMAIL_VERIFICATION should be set later
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_USERNAME_MIN_LENGTH = 5
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SESSION_REMEMBER = False
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 10
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 43200 # limit logging in for a half day
ACCOUNT_LOGOUT_REDIRECT_URL ='/'
LOGIN_REDIRECT_URL = '/'


# Summernote config
X_FRAME_OPTIONS = 'SAMEORIGIN'
SUMMERNOTE_CONFIG = {
    'summernote': {
        'width': '100%',
        'height': '480',
    }
}


# MPTT
MPTT_ADMIN_LEVEL_INDENT = 50

# internationalization
LOCALE_PATHS = [
    str(BASE_DIR.joinpath('locale')),
]


# CACHE
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": "redis://172.26.0.1:6379/1",
        # Since it changes every time containers are run
        "LOCATION": f'redis://{INTERNAL_IPS[0]}:6379/1',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
    }
}

CACHE_TTL = 60 * 15