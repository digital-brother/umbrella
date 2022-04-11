import os
from os.path import join
from pathlib import Path

import environ
from configurations import Configuration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Replacement for BASE_DIR
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
env = environ.Env()

# OS environment variables take precedence over variables from .env
DOT_ENV_FILE_PATHS = env.list('DJANGO_DOT_ENV_FILE_PATHS', default=[])
for dot_env_file_path in DOT_ENV_FILE_PATHS:
    env.read_env(str(ROOT_DIR / dot_env_file_path))


class Common(Configuration):
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # Third party apps
        'rest_framework',            # utilities for rest apis
        'rest_framework.authtoken',  # token authentication
        'django_filters',            # for filtering rest endpoints
        'drf_spectacular',
        'drf_spectacular_sidecar',
        'django_extensions',
        'corsheaders',

        # https://mozilla-django-oidc.readthedocs.io/en/stable/installation.html
        'mozilla_django_oidc',

        # Your apps
        'umbrella.users',
        'umbrella.contracts',
        'umbrella.tasks',
    )

    # https://docs.djangoproject.com/en/2.0/topics/http/middleware/
    MIDDLEWARE = (
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ALLOWED_HOSTS = ["*"]
    CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[]),
    ROOT_URLCONF = 'config.urls'
    SECRET_KEY = env("SECRET_KEY", default=None)
    WSGI_APPLICATION = 'config.wsgi.application'

    # Email
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    ADMINS = (
        ('Author', 'shuryhin.oleksandr@gmail.com'),
    )

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('POSTGRES_DATABASE'),
            'USER': env('POSTGRES_USER'),
            'PASSWORD': env('POSTGRES_PASSWORD'),
            'HOST': env('POSTGRES_HOST'),
            'PORT': env('POSTGRES_PORT', default=5432),
        }
    }

    # General
    APPEND_SLASH = False
    TIME_ZONE = 'UTC'
    LANGUAGE_CODE = 'en-us'
    # If you set this to False, Django will make some optimizations so as not
    # to load the internationalization machinery.
    USE_I18N = False
    USE_L10N = True
    USE_TZ = True
    LOGIN_REDIRECT_URL = '/'

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.0/howto/static-files/
    STATIC_ROOT = os.path.normpath(join(os.path.dirname(BASE_DIR), 'static'))
    STATICFILES_DIRS = []
    STATIC_URL = '/static/'
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    # Media files
    MEDIA_ROOT = join(os.path.dirname(BASE_DIR), 'media')
    MEDIA_URL = '/media/'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': STATICFILES_DIRS,
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

    # Set DEBUG to False as a default for safety
    # https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = env.bool('DJANGO_DEBUG', default=False)

    # Password Validation
    # https://docs.djangoproject.com/en/2.0/topics/auth/passwords/#module-django.contrib.auth.password_validation
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

    # Logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'django.server': {
                '()': 'django.utils.log.ServerFormatter',
                'format': '[%(server_time)s] %(message)s',
            },
            "verbose": {
                "format": "%(levelname)s %(asctime)s %(module)s %(message)s"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'handlers': {
            'django.server': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'django.server',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'maxBytes': 15 * 1024 * 1024,
                'filename': str(ROOT_DIR / "django.log"),
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'propagate': True,
            },
            'django.server': {
                'handlers': ['django.server'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['mail_admins', 'console'],
                'level': 'ERROR',
                'propagate': False,
            },
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'INFO'
            },
            'load_aws_analytics_jsons_to_db': {
                'handlers': ['file', 'console'],
                'level': 'INFO'
            },
        }
    }

    # Custom user app
    AUTH_USER_MODEL = 'users.User'

    # Django Rest Framework
    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': env.int('DJANGO_PAGINATION_LIMIT', default=1000),
        'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S%z',
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ),
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.TokenAuthentication',
            'umbrella.users.auth.DynamicRealmOIDCAuthentication',
        ),
        'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    }
    OIDC_DRF_AUTH_BACKEND = 'umbrella.users.auth.DynamicRealmOIDCAuthenticationBackend'

    # mozilla-django-oidc settings
    OIDC_RP_CLIENT_ID = None    # Because OIDC auth flow is done on front end side
    OIDC_RP_CLIENT_SECRET = None    # Because OIDC auth flow is done on front end side
    OIDC_OP_TOKEN_ENDPOINT = None    # Set dynamically in umbrella.users.auth.DynamicRealmOIDCAuthentication
    OIDC_OP_USER_ENDPOINT = None    # Set dynamically in umbrella.users.auth.DynamicRealmOIDCAuthentication

    OIDC_OP_TOKEN_ENDPOINT_TEMPLATE = "{keycloak_realm_url}/protocol/openid-connect/token"
    OIDC_OP_USER_ENDPOINT_TEMPLATE = "{keycloak_realm_url}/protocol/openid-connect/userinfo"

    SPECTACULAR_SETTINGS = {
        'TITLE': 'Umbrella ',
        'VERSION': '1.0.0',
        'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
        'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
        'REDOC_DIST': 'SIDECAR',
    }

    AWS_CONTRACT_BUCKET_NAME = env('AWS_CONTRACT_BUCKET_NAME', default=None)
    ALLOWED_FILE_UPLOAD_EXTENSIONS = ('.pdf', '.docx', '.doc', '.txt', '.jpeg')
    AWS_DOWNLOADS_LOCAL_ROOT = Path(env('AWS_DOWNLOADS_LOCAL_ROOT'))

    # Celery
    # ------------------------------------------------------------------------------
    if USE_TZ:
        # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-timezone
        CELERY_TIMEZONE = TIME_ZONE
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url
    CELERY_BROKER_URL = "redis://redis:6379"
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_backend
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-accept_content
    CELERY_ACCEPT_CONTENT = ["json"]
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-task_serializer
    CELERY_TASK_SERIALIZER = "json"
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_serializer
    CELERY_RESULT_SERIALIZER = "json"
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-time-limit
    # TODO: set to whatever value is adequate in your circumstances
    CELERY_TASK_TIME_LIMIT = 5 * 60
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-soft-time-limit
    # TODO: set to whatever value is adequate in your circumstances
    CELERY_TASK_SOFT_TIME_LIMIT = 60
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-scheduler
    CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
