"""
Django settings for ShopKaset project.
Generated by 'django-admin startproject' using Django 4.1.
For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from email.mime import base
import os

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

#keep the secret key used in production secret
SECRET_KEY = os.environ.get('SECRET_KEY', 'some_random_default_string')

#don't run with debug turned on in production
DEBUG = os.environ.get('DEBUG',False)

# ALLOWED_HOSTS = ['192.168.1.100']

STATIC_URL='/static/'
STATIC_ROOT=os.path.join(BASE_DIR,'static')
MEDIA_URL='/media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'static','media')

# Application definition

INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store01',
    'django.contrib.humanize',
    'crispy_forms',
    "daterange.apps.DateRangeFilterConfig",
    'stripe',
    'qrcode',
    "admincharts",
    'customAdmin'
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

ROOT_URLCONF = 'ShopKaset.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'Template')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store01.context_processors.menu_links',
                'store01.context_processors.counter',
            ],
        },
    },
]

WSGI_APPLICATION = 'ShopKaset.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storedb_kaset',
        'USER': 'root',
        'PASSWORD' :'',
        'HOST':'localhost',
        'PORT':'',
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'th-th'

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CRISPY_TEMPLATE_PACK = 'bootstrap4'

PUBLIC_KEY='pk_test_51LjbQAKNvfSPesoknPatEsVOz23ULkl4ihlVCw0N9Uc8hyIsqicMWw1rEzFRxraNKw1M5Zl5y6cClw78r0va0HiS00OL5uW4Uf'
SECRET_KEY='sk_test_51LjbQAKNvfSPesokfssnxtJYyKHIm4HGe4Bn0JIpUzz17NqVXsZbtT72PkHRgyMfwbWm2KWjySlEVjcNdzCCII0600o1znUuH1'
