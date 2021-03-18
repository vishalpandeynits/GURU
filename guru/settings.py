from pathlib import Path
import os
from decouple import config

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
SECRET_KEY = config('SECRET')
SITE_ID = config('SITE')
ALLOWED_HOSTS = ['*']

PRODUCTION = config('PROD', default=False, cast=bool)
DEBUG = config('DEBUG', default=False, cast=bool)
HTML_MINIFY = False
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #myapps
    'basic.apps.BasicConfig',
    'users.apps.UsersConfig',
    'poll.apps.PollConfig',

    #packages
    'django.contrib.humanize',
    'django.contrib.sites',
    'django_comments',
    'django_quill',
    'rest_framework',
    'crispy_forms',
    "django_filters",
    'storages',
    'imagekit',
    'notifications',
    "anymail",

    #all auth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
]

ROOT_URLCONF = 'guru.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS' : True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                "basic.context_preprocess.data",
            ],
            # 'loaders': [
            # ('django.template.loaders.cached.Loader', [
            #     'django.template.loaders.filesystem.Loader',
            #     'django.template.loaders.app_directories.Loader',
            # ])],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'guru.emaillogin.EmailBackend',
)

WSGI_APPLICATION = 'guru.wsgi.application'

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

TIME_ZONE = 'Asia/Calcutta'
USE_I18N = True

USE_L10N = True

USE_TZ = True

DJANGO_NOTIFICATIONS_CONFIG = { 'USE_JSONFIELD': True}

QUILL_CONFIGS = {
    'default':{
        'theme': 'snow',
        'modules': {
            'syntax': True,
            'toolbar': [
                [
                    {'font': []},
                    { 'size': ['small', 'large', 'huge'] },
                    {'header': []},
                    {'align': []},
                    {'image':[]},
                    
                    'bold', 'italic', 'underline', 'strike','link','blockquote','code-block',
                    {'color': []},
                    {'background': []},
                    { 'list': 'ordered'}, { 'list': 'bullet' },
                ]
            ]
        },
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGIN_REDIRECT_URL ='/homepage/'
LOGOUT_REDIRECT_URL = '/'

#all-auth registraion settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_UNIQUE_EMAIL=True
ACCOUNT_USERNAME_MIN_LENGTH = 5
ACCOUNT_USERNAME_REQUIRED =False
ACCOUNT_USERNAME_VALIDATORS = None

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

#REST FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

if PRODUCTION:
    EMAIL_HOST= "smtp.gmail.com"
    EMAIL_HOST_USER= config('EMAIL')
    EMAIL_HOST_PASSWORD= config('PASSWORD')
    EMAIL_PORT= 587
    EMAIL_USE_TLS= True
    DEFAULT_FROM_EMAIL= config('EMAIL')
    EMAIL_BACKEND = "anymail.backends.mailjet.EmailBackend"
    ANYMAIL = {
        "MAILJET_API_KEY": config('MAILJET_API_KEY'),
        "MAILJET_SECRET_KEY": config('MAILJET_SECRET_KEY'),
    }
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=10',
    }
    AWS_LOCATION = 'media'
    AWS_QUERYSTRING_AUTH=True
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    SITE_NAME = 'https://nits-class.herokuapp.com'
    AWS_PRIVATE_MEDIA_LOCATION = 'private'
    PRIVATE_FILE_STORAGE = 'guru.storage_back.PrivateMediaStorage'

    AWS_PUBLIC_MEDIA_LOCATION ='public'
    PUBLIC_FILE_STORAGE = 'guru.storage_back.PublicMediaStorage'

    AWS_S3_REGION_NAME = 'ap-south-1'
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':config('DBNAME'),
        'USER':config('USER'),
        'PASSWORD':config('DBPASS'),
        'PORT':config('DBPORT'),
        'HOST':config('DBHOST'),
    }
}
else:
    MEDIA_URL = 'media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    SITE_NAME = 'http://127.0.0.1:8000'
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
