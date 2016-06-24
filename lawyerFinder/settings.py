"""
Django settings for lawyerFinder project.

Generated by 'django-admin startproject' using Django 1.8.12.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import ConfigParser
reload(sys)
sys.setdefaultencoding("utf-8")
#from models import User

#/home/nelley/dj_pj_NL/lawyerFinder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0g26ebv$%$dig6oazgng2#p9d=#axmz*j0076+_8qnb7rc^jv^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'bootstrap3',
    'lawyerFinder',
    'accounts',
    'common',
    
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'lawyerFinder.middleware.session_controller_middleware.SessionControllerMiddleware'
    
)

#SESSION_COOKIE_AGE = 60 #second
#avoid datetime.datetime is not JSON serializable 
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

ROOT_URLCONF = 'lawyerFinder.urls'
AUTH_USER_MODEL = 'accounts.User'

MEDIA_ROOT = os.path.join(BASE_DIR, 'lawyerFinder/media')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR + '/templates'],
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

WSGI_APPLICATION = 'lawyerFinder.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        
        'NAME': 'lawyerFinder',
        'USER': 'root',
        'PASSWORD': '',
        #'HOST': '192.168.10.121',
        'HOST': '192.168.43.215',
        
        #'NAME': 'namimoch_lawyerFinder',
        #'USER': 'namimoch_root',
        #'PASSWORD': '143Nami0016Mochi!',
        #'HOST': '50.87.248.134',
        
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8',
        },
    }
}


#LOGIN_REDIRECT_URL = '/accounts'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
from django.utils.translation import ugettext_lazy as _

# python manage.py makemessages(generate xxxx.po file)
# python manage.py compilemessages(compile xxxx.po to mo file)
LANGUAGES = [
    ('ja', _('Japanease')),
    ('zh-TW', _('Traditional Chinese')),
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGE_CODE = 'zh-TW'
#LANGUAGE_CODE = 'en'
TIME_ZONE = 'Asia/Taipei'
#translation system should be enabled
USE_I18N = True
USE_L10N = True

#timezone-aware by default or not
USE_TZ = False


# AWS SES
config = ConfigParser.ConfigParser()
config.read("/home/nelley/.aws/credentials.txt")
AWS_ACC_KEY_ID = config.get("DEFAULT","aws_access_key_id")
AWS_SEC_ACC_KEY = config.get("DEFAULT","aws_secret_access_key")



MEDIA_BANNER_IMAGE_VALID_FILETYPES = (
    'JPEG', 'GIF', 'PNG'
)
MEDIA_BANNER_IMAGE_WIDTH  = 250
MEDIA_BANNER_IMAGE_HEIGHT = 250
MEDIA_BANNER_IMAGE_MAX_UPLOAD_SIZE = 4*1024*1024

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# for real enviroment(python manage.py collectstatic)
STATIC_ROOT = os.path.join(BASE_DIR, 'lawyerFinder/static')

STATIC_URL = '/static/'

# for general usage in dev
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "projectstatic"),
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s %(module)s] %(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
# form compitability with bootstrap 
from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {message_constants.DEBUG: 'debug',
                message_constants.INFO: 'info',
                message_constants.SUCCESS: 'success',
                message_constants.WARNING: 'warning',
                message_constants.ERROR: 'danger',}

# custom parameter(1*60(sec))
SESSION_FRONT_AGE = 1*60
SESSION_BACK_AGE = 1*60