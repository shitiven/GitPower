# Django settings for GitPower project.

import os, time, djcelery
from conf import *

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '9!jhbsky3%o74gplb_ny$9p&amp;2_$8-xu5nd+ktwn5twri9)#sc2'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'Common.RepoAccessMiddleWare.RepoAccessMiddleWare',
    'd403handler.middleware.D403Middleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    'django.core.context_processors.request',
    "django.contrib.messages.context_processors.messages"
)


ROOT_URLCONF = 'GitPower.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'GitPower.wsgi.application'

TEMPLATE_DIRS = (
    "%s/Templates"%os.getcwd(),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.markup',
    'south',
    'djcelery',
    'pipeline',
    'Common',
    'Pull',
    'Service',
    'Depot',
    'Account',
    'NewsFeed',
    'Issues',

    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

handler404 = 'GitPower.views.view404'

handler500 = 'GitPower.views.view500'

handler403 = 'GitPower.views.view403'

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

#profile module
AUTH_PROFILE_MODULE = 'Account.UserProfile'

#static files config
STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

STATICFILES_DIRS = (
    ('css', os.path.join(STATIC_ROOT, 'css')),
    ('js', os.path.join(STATIC_ROOT, 'js')),
)

PIPELINE = True


PIPELINE_CSS = {
    'master' : {
        'source_filenames' : (
            'css/bootstrap.css',  
            'css/bootstrap-responsive.css',
            'css/main.css',
            'css/icon.css',
            'css/jquery-ui.css',
            'css/pygments.css',
        ),
        'output_filename' : 'css/master.min.css',
    },
}

PIPELINE_JS = {
    'master' : {
        'source_filenames' : (
            'js/jquery.js', 
            'js/jquery-ui.js',
            'js/bootstrap.js',
            'js/markdown.js',
            'js/main.js',
        ),
        'output_filename' : 'js/master.min.js',
    },
}

