import os
from pathlib import Path

import pyrebase
from dotenv import load_dotenv
from marshmallow import Schema, fields, validates_schema

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)

env_path = Path('./main') / '.env'
load_dotenv(env_path)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a!x5k473)exg!d@mb0gs^81!u9p*ub2l-u&4hq%02e%!!g546r'


class EnvVarsValidator(Schema):
    CITIX_DEBUG = fields.Boolean(missing=True)

    ENABLE_FIREBASE = fields.String(missing=False)
    FIREBASE_API_KEY = fields.String(missing=None)
    FIREBASE_AUTH_DOMAIN = fields.String(missing=None)
    FIREBASE_DATABASE_URL = fields.String(missing=None)
    FIREBASE_STORAGE_BUCKET = fields.String(missing=None)

    @validates_schema
    def validate_data(self, data):
        missing_fields = []

        if data['ENABLE_FIREBASE']:
            if data['FIREBASE_API_KEY'] is None:
                missing_fields.append('FIREBASE_API_KEY')

            if data['FIREBASE_AUTH_DOMAIN'] is None:
                missing_fields.append('FIREBASE_AUTH_DOMAIN')

            if data['FIREBASE_DATABASE_URL'] is None:
                missing_fields.append('FIREBASE_DATABASE_URL')

            if data['FIREBASE_STORAGE_BUCKET'] is None:
                missing_fields.append('FIREBASE_STORAGE_BUCKET')


ENV_VARS = EnvVarsValidator().load(os.environ)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENV_VARS['CITIX_DEBUG']

ALLOWED_HOSTS = []

# Application definition

CORE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

CONTRIB_APPS = [
    'rest_framework_swagger',
    'rest_framework',
]

CUSTOM_APPS = [
    'apps.authentication'
]

INSTALLED_APPS = CORE_APPS + CONTRIB_APPS + CUSTOM_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

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

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

# Firebase

if ENV_VARS['ENABLE_FIREBASE']:
    FIREBASE_API_KEY = ENV_VARS['FIREBASE_API_KEY']
    FIREBASE_AUTH_DOMAIN = ENV_VARS['FIREBASE_AUTH_DOMAIN']
    FIREBASE_DATABASE_URL = ENV_VARS['FIREBASE_DATABASE_URL']
    FIREBASE_STORAGE_BUCKET = ENV_VARS['FIREBASE_STORAGE_BUCKET']


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
