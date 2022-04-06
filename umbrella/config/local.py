import os

from .common import Common, env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Local(Common):
    DEBUG = True

    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS + ('debug_toolbar', )
    MIDDLEWARE = Common.MIDDLEWARE + ("debug_toolbar.middleware.DebugToolbarMiddleware", )
    INTERNAL_IPS = ["127.0.0.1"]

    # Mail
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ])
