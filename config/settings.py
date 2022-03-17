"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import json
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)w#0mg=6_phw$@s*-dw=dumtu&tk4$nit$0clpvt6snq18)-s$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'user',
    'info',
    'product',
    'community',
    'game',

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # enabled providers
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.google',
]

# allauth 설정
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ACCOUNT_SIGNUP_REDIRECT_URL = 'home'  # 회원가입 후 리디렉션
LOGIN_REDIRECT_URL = 'home'  # 로그인 후 리디렉션
ACCOUNT_LOGOUT_REDIRECT_URL = 'home'  # 로그아웃시 리디렉션 reverse_lazy('user:home')
ACCOUNT_LOGOUT_ON_GET = True  # 로그아웃 버튼 클릭 시 바로 로그아웃

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"  # 이메일 검사. 임시로 none -> “mandatory” req
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # 이메일로 로그인

ACCOUNT_SESSION_REMEMBER = True  # 로그인(세션) 유지
SESSION_COOKIE_AGE = 86400  # 쿠키 하루동안 저장 -> 세션 정보 제거 python manage.py clearsessions 자동화 req

ACCOUNT_SIGNUP_FORM_CLASS = 'user.forms.SignupForm'
ACCOUNT_USERNAME_VALIDATORS = 'user.validators.custom_username_validators'
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

with open(os.path.join(BASE_DIR, 'config/social.json')) as f:
    social = json.loads(f.read())

SOCIALACCOUNT_PROVIDERS = {
    'kakao': {
        'APP': {
            'client_id': social['KAKAO']['CLIENT_ID'],
            'redirect_uri': '/redirect/',
            'response_type': '',
        }
    },
    "google": {
        "APP": {
            "client_id": social['GOOGLE']['CLIENT_ID'],
            "secret": social['GOOGLE']['SECRET'],
            "key": ""
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        }
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
    {
        "NAME": "user.validators.CustomPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-US'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "user.User"
