from .common import *
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = 'django-insecure-+$yd6o6xdowqn#%o6p-gsi64x10$l%6g!x@+f=eq8=^xngy2e&'
DEBUG = True

HOST_NAME = '127.0.0.1'

INTERNAL_IPS = [
    "127.0.0.1",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'movies',
        'USER': 'zhoma',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'TEST': {
            'USER': 'default_test',
            'TBLSPACE': 'default_test_tbls',
            'TBLSPACE_TMP': 'default_test_tbls_tmp',
        },
    }
}

EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']