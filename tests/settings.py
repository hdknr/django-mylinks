SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'mylinks',
    'tests',
    'django_nose',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.sqlite3',
        'TEST_NAME': 'test.sqlite3',
        # 'NAME': ':memory:',
    }
}
SITE_ID = 1
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
            ],
        },
    },
]
ROOT_URLCONF = 'tests.urls'
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
