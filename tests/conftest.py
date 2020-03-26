import pytest
from django.conf import settings
from django.conf import global_settings

default_settings = {
    var: value for var, value in vars(global_settings).items()
    if var.isupper()
}
default_settings['DATABASES'] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
default_settings['INSTALLED_APPS'] = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sidebar_menu',
    'tests',
]
default_settings['TEMPLATES'] = [
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


def pytest_configure():
    settings.configure(**default_settings)


@pytest.fixture
def dj_asserts():
    from django.test import TestCase
    testcase = TestCase()

    class Asserts:
        html_equal = testcase.assertHTMLEqual

    return Asserts()
