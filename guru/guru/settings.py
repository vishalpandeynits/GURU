"""
Django settings for guru project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*j)kfw7j9ltu!=t$o0@4m!umac+&j#3)q^*j_g%z%qpwoeh=9d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SITE_ID = 2
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_email_verification',
    'basic.apps.BasicConfig',
    'users.apps.UsersConfig',
    'crispy_forms',
    'django.contrib.humanize',
    'bootstrap_datepicker_plus',
    'django.contrib.sites',
    'django_comments',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
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

ROOT_URLCONF = 'guru.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'guru.emaillogin.EmailBackend',
)

WSGI_APPLICATION = 'guru.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = 'statica'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
LOGIN_REDIRECT_URL ='/homepage/'
LOGOUT_REDIRECT_URL='https://www.google.com/'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_ACTIVE_FIELD = 'is_active'
EMAIL_SERVER = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_ADDRESS = 'vishalpandeynits@gmail.com'
EMAIL_FROM_ADDRESS = 'vishalpandeynits@gmail.com'
EMAIL_PASSWORD = '*******************' # Use your password here
EMAIL_MAIL_SUBJECT = 'Confirm your email'
EMAIL_MAIL_HTML = 'mail_body.html'
EMAIL_MAIL_PLAIN = 'mail_body.txt'
EMAIL_PAGE_TEMPLATE = 'confirm_template.html'
EMAIL_PAGE_DOMAIN = 'http://127.0.0.1:8000/'

# CKEDITOR_UPLOAD_PATH = 'uploads/'
# CKEDITOR_CONFIGS = {
#         'default': {
#         'skin': 'moono',
#         'toolbar_Basic': [
#             ['Source',  'Bold', 'Italic']
#         ],
#         'toolbar_YourCustomToolbarConfig': [
#             {'name': 'editing', 'items': ['Find', 'Replace', 'SelectAll']},

#             {'name': 'basicstyles',
#              'items': ['Bold', 'Italic', 'Underline', 'Strike']},

#             {'name': 'insert',
#              'items': ['Image',  'Table', 'Smiley', 'SpecialChar',]},

#             {'name': 'paragraph',
#              'items': ['NumberedList', 'BulletedList', 'Blockquote',
#                        'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'BidiLtr', 'BidiRtl',]},
#             {'name': 'colors', 'items': ['TextColor', 'BGColor']},

#             {'name': 'styles', 'items': [ 'Format', 'Font', 'FontSize']},

#             ],
#         'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
#         'height': 300,
#         'width': '100%;',
#         'filebrowserWindowHeight': 725,
#         'filebrowserWindowWidth': 940,
#         'toolbarCanCollapse': True,
#         'tabSpaces': 4,
#     }
# }
#all-auth registraion settings
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS =1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400 # 1 day.
LOGOUT_REDIRECT_URL = 'http://127.0.0.1:8000/'
ACCOUNT_PRESERVE_USERNAME_CASING = False # reduces the delays in iexact lookups
ACCOUNT_UNIQUE_EMAIL=True
ACCOUNT_USERNAME_MIN_LENGTH = 5
ACCOUNT_USERNAME_REQUIRED =False
ACCOUNT_USERNAME_VALIDATORS = None

# #Account adapters
# ACCOUNT_ADAPTER = 'allauthdemo.adapter.CustomProcessAdapter'

# #Account Signup
# ACCOUNT_FORMS = {'signup': 'allauthdemo.forms.SignupForm',}

#Social Account Settings
SOCIALACCOUNT_PROVIDERS = {
     'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}
SOCIALACCOUNT_QUERY_EMAIL=ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_EMAIL_REQUIRED=ACCOUNT_EMAIL_REQUIRED
SOCIALACCOUNT_STORE_TOKENS=False