import os
from pathlib import Path

from django.templatetags import static
from django.urls import reverse, reverse_lazy
from channels_redis.core import RedisChannelLayer

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@g7fo9j*=k!2(&#9uvuw-mk#pu&kgc3_js#3uiu1r@90ysyfrj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'mysite.com']


# Application definition

INSTALLED_APPS = [
    'daphne',
    'test_chat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',
    'post.apps.PostConfig',
    'comment.apps.CommentConfig',
    'article.apps.ArticleConfig',
    'rating.apps.RatingConfig',
    'chats.apps.ChatsConfig',
    'social_django',
    'django_extensions',
    'debug_toolbar',
    'channels'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'meetmax.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

ASGI_APPLICATION = 'meetmax.asgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# Django channels
ASGI_APPLICATION = 'meetmax.asgi.application'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'accounts.authentication.EmailAuthBackend',
    'social_core.backends.facebook.FacebookOAuth2',
    'accounts.authentication.AuthenticationGoogleView',
    'social_core.backends.twitter.TwitterOAuth',
]

SOCIAL_AUTH_PIPELINE = [
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
]

# google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '833675845573-92ni3fmf7u721c8k5nrqrq516bch9olo.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

# twitter
SOCIAL_AUTH_TWITTER_KEY = 'CiWsTfcDzJ9GNmWnHqLiRrKkQ'
SOCIAL_AUTH_TWITTER_SECRET = 'lDwI8tv8HSE0M6Ga221QBCiuyss31jTYWMMbT2587EVGPcgeEU'

# facebook
SOCIAL_AUTH_FACEBOOK_KEY = '1306486754081101'
SOCIAL_AUTH_FACEBOOK_SECRET = 'b21872b8dbaee90fab4fa364f0e58341'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

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

# smtp

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_USER = 'begzodbey0426@gmail.com'

EMAIL_HOST_PASSWORD = 'vlzdgrwdugibijdy'

't@LU6usb_hSC8w'

EMAIL_PORT = 587

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

EMAIL_USE_TLS = True

EMAIL_USE_SSL = False

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'main_static'),
]
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = reverse_lazy('posts_list')

LOGIN_URL = reverse_lazy('accounts:sing_in')

# debug_tool/settings.py

INTERNAL_IPS = [
    '127.0.0.1',
]
