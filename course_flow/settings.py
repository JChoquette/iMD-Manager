"""
Django settings for course_flow_maker project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

SECRET_KEY = "course_flow"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

CHROMEDRIVER_PATH = None

# Application definition

TEACHER_GROUP = "Teacher"

ADMINS = [("John", "john@example.com"), ("Mary", "mary@example.com")]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS = [
    "compressor",
    "django_lti_tool_provider",
    "user_feedback.apps.UserFeedbackConfig",
    "course_flow.apps.CourseFlowConfig",
    "rest_framework",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
]

ROOT_URLCONF = "course_flow.test_urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

CSP_INCLUDE_NONCE_IN = [
    "script-src",
    "style-src",
]
CSP_DEFAULT_SRC = ["'self'", "*.mydalite.org"]
CSP_SCRIPT_SRC = [
    "'self'",
    "*.mydalite.org",
    "d3js.org",
    "ajax.googleapis.com",
    "cdn.polyfill.io",
    "cdn.quilljs.com",
]
CSP_STYLE_SRC = [
    "'self'",
    "*.mydalite.org",
    "ajax.googleapis.com",
    "cdn.quilljs.com",
    "fonts.googleapis.com",
]
CSP_FONT_SRC = [
    "'self'",
    "*.mydalite.org",
    "fonts.gstatic.com",
]

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "course_flow:home"
LOGOUT_REDIRECT_URL = "login"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

ADMINS = [("John", "john@example.com"), ("Mary", "mary@example.com")]

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

GRAPH_MODELS = {"all_applications": True, "group_models": True}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttribute"
        "SimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "server_static/")

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication"
    ]
}

# For LTI tests
PASSWORD_KEY = "course_flow"
LTI_CLIENT_KEY = "course_flow"
LTI_CLIENT_SECRET = "course_flow"

"""
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(name)s - %(levelname)s - %(asctime)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "simple",
            "filename": os.path.join(BASE_DIR, "logs"),
        },
        "console": {
            "level": "DEBUG" if DEBUG else "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": True,
        },
        "courseflow": {
            "handlers": ["console", "file"],
            "level": "DEBUG" if DEBUG else "INFO",
        },
    },
}
"""

try:
    from .local_settings import *  # noqa F403

    try:
        INSTALLED_APPS += LOCAL_APPS  # noqa F405
    except NameError:
        pass
except ImportError:
    import warnings

    warnings.warn(
        "File local_settings.py not found. You probably want to add it -- "
        "see README.md."
    )
    pass
