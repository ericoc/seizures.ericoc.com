"""
Django settings for seizures project.
"""
from pathlib import Path
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Administrators/email
ADMINS = [('Eric OC', 'eric@ericoc.com')]
EMAIL_HOST = 'localhost'
SERVER_EMAIL = 'django@ericoc.com'
DEFAULT_FROM_EMAIL = 'django@ericoc.com'

# Default look-back timespan
DEFAULT_SINCE = timedelta(hours=24)

# Apple device icons
DEVICE_ICONS = {'Mac': '💻', 'iPhone': '📱', 'Watch': '⌚'}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'EXAMPLE'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ("seizures.ericoc.com",)

# CSRF settings
CSRF_COOKIE_DOMAIN = ALLOWED_HOSTS[0]
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = ("https://seizures.ericoc.com",)

# Language cookie settings
LANGUAGE_COOKIE_SECURE = True

# SSL settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_HOST = ALLOWED_HOSTS[0]
SECURE_SSL_REDIRECT = True


# Session cookie settings
SESSION_COOKIE_DOMAIN = ALLOWED_HOSTS[0]
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_SECURE = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'seizures.apps.SeizuresConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
]

KEY_PREFIX = 'seizures_'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = LOGIN_URL

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGE_SIZE': 50
}

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
WSGI_APPLICATION = 'wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'seizures',
        'USER': 'seizures',
        'PASSWORD': 'EXAMPLE',
        'HOST': 'localhost',
    }
}
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_TZ = True

# Static content
STATIC_URL = 'static/'
STATIC_ROOT = Path(BASE_DIR, STATIC_URL)

# Media files (user uploads)
MEDIA_URL = 'media/'
MEDIA_ROOT = Path(BASE_DIR, MEDIA_URL)

USE_THOUSAND_SEPARATOR = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
