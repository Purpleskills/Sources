"""
Django settings for psweb project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4m+tir0qka69y@^yi&1@oysnwrrr=ginkp&jq(b8#on6m^=4c1'


# SECURITY WARNING: don't run with debug turned on in production!
if 'RDS_HOSTNAME' not in os.environ:
    DEBUG = True
else:
    DEBUG = False

TEMPLATE_DEBUG = True


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = (
)


MEDIA_URL = "http://0.0.0.0:8000/media/"
MEDIA_ROOT = os.path.dirname(BASE_DIR) + "/media/"
STORAGE_URL = MEDIA_URL

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'psweb',
    'home',
    'learn',
    'contentprovider'
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'psweb.urls'

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
                # 'imagestore.context_processors.imagestore_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'psweb.wsgi.application'
ALLOWED_HOSTS = ['*']
# AUTH_USER_MODEL='sauth.SeraUser'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL='/home/'
LOGOUT_REDIRECT_URL = '/home/'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

if 'RDS_HOSTNAME' not in os.environ:

    DATABASES = {
    	'default': {
        	'ENGINE': 'django.db.backends.postgresql_psycopg2',
        	'NAME': 'purpleskillsdb',
        	'USER':  'psroot',
        	'PASSWORD': 'pswhatever1',
        	'HOST': '127.0.0.1',
       	 	'PORT': '',
    		}
	}
  
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'TIMEOUT': 300,
            'OPTIONS': {
                'MAX_ENTRIES': 200
            }
        }
    }

    DEBUG_TOOLBAR_PANELS = [
        # 'ddt_request_history.panels.request_history.RequestHistoryPanel',  # Here it is
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
        'debug_toolbar.panels.profiling.ProfilingDebugPanel',
    ]
    def AllowToolbar(request):
        return True


    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': 'psweb.settings.AllowToolbar',
        #'ddt_request_history.panels.request_history.allow_ajax',
        'RESULTS_STORE_SIZE': 100,
    }

    INSTALLED_APPS += (
             #'fixture_magic',
             'debug_toolbar',
             #'debug_panel',
             #'sslserver',
    )
    DEBUG_TOOLBAR_PATCH_SETTINGS = True
    MIDDLEWARE = ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'purpleskillsdb',
                'USER': 'psroot',
                'PASSWORD': 'pswhatever1',
                'HOST': os.environ['RDS_HOSTNAME'],
                'PORT': 3306,
                'OPTIONS': {
                        'charset': 'utf8mb4',
                        'use_unicode': True, },
        }
    }
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'TIMEOUT': 300,
            'OPTIONS': {
                'MAX_ENTRIES': 200
            }
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
