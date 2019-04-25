import os
import datetime
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
import emailconfig

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 't2lqmz!73beh_de106_q223gt=())x^if%p3+7r-dka&8a!nsj'

DEBUG = True

ALLOWED_HOSTS = [
    '*',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'jwt',
    'api',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}

CELERY_BROKER_URL = "amqp://rabbitmq"

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

CACHE_DEFAULT_TIMEOUT = 60

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_URL = '/static/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = 'http://0.0.0.0:8000/media/'

print(BASE_DIR)
# print(MEDIA_ROOT)
HOST_IP_ADDRESS = os.environ.get('HOST_IP_ADDRESS', '0.0.0.0')

API_KEY = 'AIzaSyB0JNTrEhvtwALjuc68NGxXCKMfiBJRVTs'
API_URL = 'https://speech.googleapis.com/v1/speech:recognize?key={}'.format(API_KEY)
API_LANGUAGE_CODE = 'ru-RU'

# todo bring back enviroment variable after i stop being lazy
PUBLIC_KEY = open('public.pem').read()
PRIVATE_KEY = open('private.pem').read()
# PRIVATE_KEY = os.environ.get('PRIVATE_KEY')

JWT_AUTH = {
    'JWT_PUBLIC_KEY': PUBLIC_KEY,
    'JWT_PRIVATE_KEY': PRIVATE_KEY,
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_ALGORITHM': 'RS256',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=6000),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',

    ),
}

AUTH_USER_MODEL = "api.User"

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = emailconfig.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = emailconfig.EMAIL_HOST_PASSWORD
EMAIL_PORT = 587


sentry_sdk.init(
    dsn="https://fcff3bd74f7045b384aae20943e6d04a@sentry.io/1445996",
    integrations=[DjangoIntegration()]
)

